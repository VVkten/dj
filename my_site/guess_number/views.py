from django.shortcuts import render
import random

def guess_number(request):
    if 'target_number' not in request.session:
        request.session['target_number'] = random.randint(1, 100)
        request.session['attempts'] = 0

    target_number = request.session['target_number']
    attempts = request.session['attempts']

    message = ''
    if 'guess' in request.GET:
        try:
            user_guess = int(request.GET['guess'])
            attempts += 1
            request.session['attempts'] = attempts

            if user_guess < target_number:
                message = 'Занадто мало!'
            elif user_guess > target_number:
                message = 'Занадто багато!'
            else:
                message = f'Вітаємо! Ви вгадали число за {attempts} спроб!'
                # Починаємо нову гру
                del request.session['target_number']
                del request.session['attempts']
        except ValueError:
            message = 'Будь ласка, введіть число.'
    return render(request, 'guess_number/guess.html', {'message': message, 'attempts': attempts})

