# hello/views.py
from django.shortcuts import render

def hello_name(request):
    return render(request, 'hello/hello.html')

# def calc(request):
#     # a = int(request.GET.get('a', 0))
#     # b = int(request.GET.get('b', 0))
#     # result = a + b
#     return render(request, 'hello/calc.html')


# def guess_number(request):
#     # Якщо гра ще не почалась, ініціалізуємо сесію
#     if 'target_number' not in request.session:
#         request.session['target_number'] = random.randint(1, 100)
#         request.session['attempts'] = 0
#
#     target_number = request.session['target_number']
#     attempts = request.session['attempts']
#
#     message = ''
#     if 'guess' in request.GET:
#         try:
#             user_guess = int(request.GET['guess'])
#             attempts += 1
#             request.session['attempts'] = attempts
#
#             if user_guess < target_number:
#                 message = 'Занадто мало!'
#             elif user_guess > target_number:
#                 message = 'Занадто багато!'
#             else:
#                 message = f'Вітаємо! Ви вгадали число за {attempts} спроб!'
#                 # Починаємо нову гру
#                 del request.session['target_number']
#                 del request.session['attempts']
#         except ValueError:
#             message = 'Будь ласка, введіть число.'
#     return render(request, 'hello/guess.html', {'message': message, 'attempts': attempts})
