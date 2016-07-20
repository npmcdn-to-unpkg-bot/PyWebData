import os
from django.shortcuts import render
from .analyze import colorz as cz
from .models import Files, Colors, Personality

def update(request):
    img_dir = 'static/img/'
    for file in os.listdir(img_dir): #해당 디렉터리에 있는 파일들의 리스트
        db_file = Files(filename=file)
        db_file.save() # db_file을 저장한다.
        rgbs = cz(img_dir+file) #RGB값을 리턴한다.
        rgb_str = ''
        for rgb in rgbs:
            rgb_str = '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])
        colors = Colors(rgb=rgb_str, red=rgb[0], green=rgb[1], blue=rgb[2]) #Colors에 rgb값과 red , green ,blue의 값을 넣는다.
        colors.file_id = db_file.id #db아이디 값을 넣는다.
        colors.save() #저장한다.

def index(request): # result.html
    script = '''<script src="https://npmcdn.com/masonry-layout@4.0/dist/masonry.pkgd.min.js"></script>'''
    files = Files.objects.all() #models 에 있는 Files를 가져온다.
    size = {'width':100, 'height':200} #이미지 사이즈를 설정한다.
    return render(request, 'select_picture.html', {'script':script, 'files':files, 'size':size})

def result(request, pic_id):
    pic_color = Colors.objects.all().filter(file_id=pic_id) #Colors에서 입력된 아이의 값을 찾아 Pic_Color에 대입하낟.
    pic_color = pic_color.values()[0] #0번째 값만 저장한다.
    pic_color = (pic_color['red'], pic_color['green'], pic_color['blue'],)
    personalities = Personality.objects.all() # 성격데이터를 가져온다.
    colors = {}
    for personality in personalities.values():
        colors[personality['rgb']] = (personality['red'], personality['green'], personality['blue'],)
    euclidean = lambda x, y: (x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2 + (x[2] - y[2]) ** 2
    distances = {k: euclidean(v, pic_color) for k, v in colors.items()}
    rgb_hex = min(distances, key=distances.get)

    for val in personalities.values():
        if val['rgb'] == rgb_hex: #rgb 값이 같을 경우
            result = val['description'] #성격내용
            break

    return render(request, 'result.html', context={'personality' : result}) #성격격과를 personality보낸다.

