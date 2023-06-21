from django.shortcuts import render
from django.views import View
import random

class BaseballGameView(View):
    template_name = 'baseball_game/game.html'

    def get(self, request):
        request.session['strikes'] = 0
        request.session['outs'] = 0
        request.session['runners'] = []
        request.session['point'] = 0
        return render(request, self.template_name)

    def post(self, request):
        pitch = int(request.POST.get('pitch',1))
        strikes = request.session.get('strikes', 0)
        outs = request.session.get('outs', 0)
        runners = request.session.get('runners', [])
        point = request.session.get('point', 0)

        ball_list = ["none", "ストレート", "スライダー", "カーブ", "フォーク", "チェンジアップ"]

        def runner_on_first():
            runners.append(1)

        def runner_on_second():
            runners.append(2)

        def runner_on_third():
            runners.append(3)

        def runner_on_base():
            runners.append(10)

        def advance_runner_to_second():
            for i in range(len(runners)):
                if runners[i] == 1:
                    runners[i] = 2

        def advance_runner_to_third():
            for i in range(len(runners)):
                if runners[i] == 1:
                    runners[i] = 3

        def advance_runner_to_forth():
            for i in range(len(runners)):
                if runners[i] == 1:
                    runners[i] = 4

        def advance_runner_on_second_to_third():
            for i in range(len(runners)):
                if runners[i] == 2:
                    runners[i] = 3

        def advance_runner_on_second_to_forth():
            for i in range(len(runners)):
                if runners[i] == 2:
                    runners[i] = 4

        def advance_runner_on_second_to_fifth():
            for i in range(len(runners)):
                if runners[i] == 2:
                    runners[i] = 5

        def advance_runner_on_third_to_forth():
            for i in range(len(runners)):
                if runners[i] == 3:
                    runners[i] = 4

        def advance_runner_on_third_to_fifth():
            for i in range(len(runners)):
                if runners[i] == 3:
                    runners[i] = 5

        def advance_runner_on_third_to_sixth():
            for i in range(len(runners)):
                if runners[i] == 3:
                    runners[i] = 6

        def remove_runner_on_first():
            for runner in runners[:]:
                if runner == 1:
                    runners.remove(runner)

        def remove_runner_on_second():
            for runner in runners[:]:
                if runner == 2:
                    runners.remove(runner)

        def remove_runner_on_third():
            for runner in runners[:]:
                if runner == 3:
                    runners.remove(runner)

        def point_get(point):
            for runner in runners[:]:
                if runner >= 4:
                    runners.remove(runner)
                    point = point + 1
                    print("得点追加！")
            return point

        def point_write(point):
            print("現在の得点は" + str(point) + "点です")

        def itiruida():
            if len(runners) > 0:
                advance_runner_on_third_to_forth()
                advance_runner_on_second_to_third()
                advance_runner_to_second()
            runner_on_first()
            print("ヒット!!!1塁打")

        def niruida():
            if len(runners) > 0:
                advance_runner_on_third_to_fifth()
                advance_runner_on_second_to_forth()
                advance_runner_to_third()
            runner_on_second()
            print("ヒット!!!2塁打")

        def sannruida():
            if len(runners) > 0:
                advance_runner_on_third_to_sixth()
                advance_runner_on_second_to_fifth()
                advance_runner_to_forth()
            runner_on_third()
            print("ヒット!!!3塁打")

        def homerun():
            if len(runners) > 0:
                advance_runner_to_forth()
                advance_runner_on_second_to_fifth()
                advance_runner_on_third_to_sixth()
            runner_on_base()
            print("ホーーームラン！！！")

        def runner_move_and_point_get(p_ball, chance):
            if p_ball == 1 or p_ball == 2 or p_ball == 4:
                print("ヒット!!!")
                if p_ball == 2 and chance == True:
                    niruida()
                else:
                    itiruida()
            elif p_ball == 5:
                if chance == True:
                    sannruida()
                else:
                    niruida()
            else:
                homerun()

        def decide_ball():
            t = random.randint(1, 100)
            if t <= 25:
                return 1
            elif t <= 50:
                return 2
            elif t <= 75:
                return 4
            elif t <= 90:
                return 5
            else:
                return 3

        def reset_game():
            request.session['strikes'] = 0
            request.session['outs'] = 0
            request.session['runners'] = []
            request.session['point'] = 0

        chance = False

        if pitch >= 1 and pitch <= 5:
            p_ball = pitch
        else:
            return render(request, self.template_name, {'error': '正しく入力してください。'})

        c_ball = decide_ball()
        c_ball_name = ball_list[c_ball]

        if c_ball - p_ball == 0:
            runner_move_and_point_get(p_ball, chance)
            point = point_get(point)
            point_write(point)
            strikes = 0
        else:
            print("\n空振り!\n\n")
            strikes += 1

        if strikes == 3:
            print("三振！アウト！\n\n")
            outs += 1
            strikes = 0

        if point >= 2:
            print("得点が入った！ゲームクリア！\n\n")
            reset_game()
            return render(request, self.template_name, {'game_status': 'clear', 'point': point})

        if outs == 3:
            print("3アウト!この回の攻撃は終了です\n\n\n")
            reset_game()
            return render(request, self.template_name, {'game_status': 'out'})

        request.session['strikes'] = strikes
        request.session['outs'] = outs
        request.session['runners'] = runners
        request.session['point'] = point

        return render(request, self.template_name, {'strikes': strikes, 'outs': outs, 'runners': runners, 'point': point,
                                                    'c_ball_name': c_ball_name})
