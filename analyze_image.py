import cv2
import operator
import numpy as np

color2pix = {
"red": [255,0,0],
"green": [0,255,0],
"blue": [0,0,255],
"yellow": [255,255,0],
"black": [0,0,0],
"orange": [255,128,0],
"purple": [255,0,255]
}

messages = {
"red": "alert, aggressive, dominant, ambitious",
"green": "adventurous, efficient",
"blue": "calmness, logical, balanced",
"yellow": "happy, aspiration, energetic",
"black": "power, mysterious, evil",
"orange": "celebrative, enduring",
"purple": "anxious, spiritual, compassionate"
}

def analysis(im_name):
    good_colours = ["green", "blue", "yellow", "orange"]

    color_present = {}
    for i in color2pix.keys():
        color_present[i] = 0
    im = cv2.imread(im_name)
    im = cv2.resize(im, (100, 100))
    im = cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
    for i in range(100):
        for j in range(100):
            if im[i][j][0]>250:
                if im[i][j][1]>250:
                    if im[i][j][2]<5:
                        color_present["yellow"] += 1
                elif im[i][j][1]>120 and im[i][j][1]<135:
                    if im[i][j][2]<5:
                        color_present["orange"] += 1
                elif im[i][j][1]<5:
                    if im[i][j][2]>250:
                        color_present["purple"] += 1
                    elif im[i][j][2]<5:
                        color_present["red"] += 1
            elif im[i][j][0]<10:
                if im[i][j][1]>250:
                    if im[i][j][2]<5:
                        color_present["green"] += 1
                if im[i][j][1]<5:
                    if im[i][j][2]<5:
                        color_present["black"] += 1
                    elif im[i][j][2]>250:
                        color_present["blue"] += 1
    total = 0
    for i in color_present.keys():
        total += color_present[i]
    for i in color_present.keys():
        color_present[i] = color_present[i]/total

    sorted_colors = sorted(color_present.items(), key=operator.itemgetter(1))
    best = sorted_colors[-1]
    best2 = sorted_colors[-2]

    try:
        good_colours.remove(best[0])
    except:
        pass
    try:
        good_colours.remove(best2[0])
    except:
        pass
    send_msg = "Mostly used "+ best[0] + " = %.2f"%best[1] + "% and " + best2[0] + " = %.2f"%best2[1] + "%\n" \
               + best[0] + " shows " + messages[best[0]] + " nature." + "\n" \
               + best2[0] + " shows " + messages[best2[0]] + " nature." + "\n" + \
               "You can try putting more " + np.random.choice(good_colours) + " colour."
    return send_msg

if __name__ == "__main__":
    print(analysis("analyze.png"))
