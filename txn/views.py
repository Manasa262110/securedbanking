from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.conf import settings
from django.db.models import Q
from reportlab.pdfgen import canvas
from decimal import Decimal, InvalidOperation
from django.contrib.auth.models import User

from cards.models import CardList
from banks.models import BankList
from accounts.models import User
from txn.models import Transactions
from txn.crypto_utils import encrypt_data, decrypt_data

key = getattr(settings, 'ENCRYPTION_KEY', 'Th1sIsA16ByteKey')


@login_required
def deposit(request):
    userdata = request.user
    cards = CardList.objects.all()
    banks = BankList.objects.all()

    if request.method == 'POST':
        try:
            name = encrypt_data(request.POST['name'], key)
            card = encrypt_data(request.POST['card'], key)
            bank = encrypt_data(request.POST['bank'], key)
            deposit_amount = Decimal(request.POST['deposit'])

            txn = Transactions.objects.create(
                to_account=userdata.username,
                from_account=userdata.username,
                name=name,
                card=card,
                bank=bank,
                txntype='Deposit',
                amount=deposit_amount
            )

            # Removed blockchain logging
            # data = f"TXN:{txn.from_account}->{txn.to_account}:{txn.amount}"
            # send_to_chain(data)

            messages.success(request, 'Amount Deposited. Balance will reflect after verification.')
            return redirect('deposit')

        except (KeyError, InvalidOperation):
            messages.error(request, 'Invalid input. Please try again.')

    return render(request, 'user/deposit.html', {
        'cards': cards,
        'banks': banks,
        'userdata': userdata
    })


@login_required
def withdraw(request):
    userdata = request.user
    cards = CardList.objects.all()
    banks = BankList.objects.all()

    if request.method == 'POST':
        try:
            name = encrypt_data(request.POST['name'], key)
            card = encrypt_data(request.POST['card'], key)
            bank = encrypt_data(request.POST['bank'], key)
            withdraw_amount = Decimal(request.POST['withdraw'])

            txns = Transactions.objects.filter(Q(from_account=userdata.username) | Q(to_account=userdata.username))
            balance = 0
            for txn in txns:
                if txn.txntype == "Deposit" and txn.from_account == txn.to_account:
                    balance += txn.amount
                elif txn.txntype == "Withdraw" and txn.from_account == txn.to_account:
                    balance -= txn.amount
                elif txn.txntype == "Transfer":
                    if txn.from_account == userdata.username:
                        balance -= txn.amount
                    elif txn.to_account == userdata.username:
                        balance += txn.amount

            if withdraw_amount <= balance:
                txn = Transactions.objects.create(
                    to_account=userdata.username,
                    from_account=userdata.username,
                    name=name,
                    card=card,
                    bank=bank,
                    txntype='Withdraw',
                    amount=withdraw_amount
                )

                # Removed blockchain logging
                # data = f"TXN:{txn.from_account}->{txn.to_account}:{txn.amount}"
                # send_to_chain(data)

                messages.success(request, 'Amount Withdrawn. Balance will reflect after verification.')
            else:
                messages.error(request, 'Insufficient Balance.')

            return redirect('withdraw')

        except (KeyError, InvalidOperation):
            messages.error(request, 'Invalid input. Please try again.')

    return render(request, 'user/withdraw.html', {
        'cards': cards,
        'banks': banks,
        'userdata': userdata
    })


@login_required
def transfer(request):
    current_user = request.user
    all_users = User.objects.exclude(username=current_user.username)
    cards = CardList.objects.all()
    banks = BankList.objects.all()

    if request.method == 'POST':
        try:
            name = encrypt_data(request.POST['name'], key)
            card = encrypt_data(request.POST['card'], key)
            bank = encrypt_data(request.POST['bank'], key)
            to_account = request.POST['to_account']
            transfer_amount = Decimal(request.POST['transfer'])

            txns = Transactions.objects.filter(Q(from_account=current_user.username) | Q(to_account=current_user.username))
            balance = 0
            for txn in txns:
                if txn.txntype == "Deposit" and txn.from_account == txn.to_account:
                    balance += txn.amount
                elif txn.txntype == "Withdraw" and txn.from_account == txn.to_account:
                    balance -= txn.amount
                elif txn.txntype == "Transfer":
                    if txn.from_account == current_user.username:
                        balance -= txn.amount
                    elif txn.to_account == current_user.username:
                        balance += txn.amount

            if transfer_amount <= balance:
                txn = Transactions.objects.create(
                    to_account=to_account,
                    from_account=current_user.username,
                    name=name,
                    card=card,
                    bank=bank,
                    txntype='Transfer',
                    amount=transfer_amount
                )

                # Removed blockchain logging
                # data = f"TXN:{txn.from_account}->{txn.to_account}:{txn.amount}"
                # send_to_chain(data)

                messages.success(request, 'Transfer Successful. Balance will reflect after verification.')
            else:
                messages.error(request, 'Insufficient Balance.')

            return redirect('transfer')

        except (KeyError, InvalidOperation):
            messages.error(request, 'Invalid input. Please try again.')

    template = 'vendor/transfer.html' if current_user.is_staff else 'user/transfer.html'
    return render(request, template, {
        'cards': cards,
        'banks': banks,
        'current_user': current_user,
        'userdata': all_users
    })


@login_required
def txnHistory(request):
    user = request.user
    txns = Transactions.objects.filter(Q(from_account=user.username) | Q(to_account=user.username)).order_by('-time')

    decrypted_txns = []
    for txn in txns:
        try:
            txn.name = decrypt_data(txn.name, key)
            txn.card = decrypt_data(str(txn.card), key)
            txn.bank = decrypt_data(txn.bank, key)
        except Exception:
            txn.name = txn.card = txn.bank = "Decryption Error"
        decrypted_txns.append(txn)

    template = 'admin/transactions.html' if user.is_superuser else (
        'vendor/transactions.html' if user.is_staff else 'user/transactions.html')

    return render(request, template, {'txns': decrypted_txns})


@login_required
def txnVerify(request, id):
    txn = get_object_or_404(Transactions, id=id)
    txn.verified = True
    txn.save()
    messages.success(request, "Transaction Verified.")
    return redirect('transactions')


@login_required
def form(request):
    return render(request, 'txn/form.html')


@login_required
def predict(request):
    return render(request, 'predict.html')


@login_required
def download_receipt(request, txn_id):
    txn = get_object_or_404(Transactions, id=txn_id)
    if txn.to_account != request.user.username and txn.from_account != request.user.username:
        return HttpResponse("Unauthorized", status=403)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=receipt_{txn_id}.pdf'

    p = canvas.Canvas(response)

    try:
        name = decrypt_data(txn.name, key)
        card = decrypt_data(txn.card, key)
        bank = decrypt_data(txn.bank, key)
    except Exception:
        name = card = bank = "Decryption Error"

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "Transaction Receipt")
    p.setFont("Helvetica", 12)
    p.drawString(50, 760, f"Transaction ID: {txn.id}")
    p.drawString(50, 740, f"From: {txn.from_account}")
    p.drawString(50, 720, f"To: {txn.to_account}")
    p.drawString(50, 700, f"Name: {name}")
    p.drawString(50, 680, f"Card: {card}")
    p.drawString(50, 660, f"Bank: {bank}")
    p.drawString(50, 640, f"Type: {txn.txntype}")
    p.drawString(50, 620, f"Amount: ₹{txn.amount}")
    p.drawString(50, 600, f"Time: {txn.time.strftime('%Y-%m-%d %H:%M:%S')}")
    p.drawString(50, 580, f"Status: {'Completed' if txn.txnstatus else 'Pending'}")

    p.showPage()
    p.save()
    return response


@login_required
def balance_view(request):
    user = request.user
    txns = Transactions.objects.filter(
        Q(from_account=user.username) | Q(to_account=user.username)
    )

    balance = 0
    for txn in txns:
        if txn.txntype == "Deposit" and txn.from_account == txn.to_account:
            balance += txn.amount
        elif txn.txntype == "Withdraw" and txn.from_account == txn.to_account:
            balance -= txn.amount
        elif txn.txntype == "Transfer":
            if txn.from_account == user.username:
                balance -= txn.amount
            elif txn.to_account == user.username:
                balance += txn.amount

    return render(request, 'user/balance.html', {'balance': balance})
