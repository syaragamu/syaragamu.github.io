from django.shortcuts import render, redirect
import random

def index(request):
    if 'target_number' not in request.session:
        # セッションにtarget_numberが存在しない場合、新しいゲームを開始
        request.session['target_number'] = random.randint(1, 100)
        request.session['guess_count'] = 0
        request.session['message'] = '新しいゲームを開始しました。1から100の間の数を当ててください。'
    return render(request, 'game_app/game.html', {'message': request.session['message'], 'csrf_token': request.COOKIES.get('csrftoken')})

def play(request):
    if request.method == 'POST':
        guess = int(request.POST['guess'])
        target_number = request.session['target_number']
        guess_count = request.session['guess_count'] + 1

        if guess < target_number:
            message = f'{guess}は正解ではありません。もっと大きな数です。'
        elif guess > target_number:
            message = f'{guess}は正解ではありません。もっと小さな数です。'
        else:
            message = f'おめでとうございます！{guess}は正解です。{guess_count}回目の予想で当たりました！'
            del request.session['target_number']
            del request.session['guess_count']

        request.session['guess_count'] = guess_count
        request.session['message'] = message

    return redirect('game_app:index')
