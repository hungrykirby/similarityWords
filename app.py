import cv2
import os

MODE = "images"
outputfilename = "results_" + MODE

"""初期化"""
IMG_DIR = os.path.abspath(os.path.dirname(__file__)) + '/' + MODE + '/'
IMG_SIZE = (250, 250)

bf = cv2.BFMatcher(cv2.NORM_HAMMING)
detector = cv2.AKAZE_create()

files = os.listdir(IMG_DIR)
imgs = []

results = []
results_sum = []

outputfile = open('output/' + outputfilename + '.csv', 'w')


"""画像の準備"""
line = [" "]
for f in files:
    line.append(f.split(".")[0])
    img = cv2.imread(IMG_DIR + f, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, IMG_SIZE)
    imgs.append({
        "image":img,
        "filename":f
    })
outputfile.writelines(",".join(line))
outputfile.writelines("\n")


"""特徴量比較"""
for target_img in imgs:
    line = [target_img["filename"].split(".")[0]]
    (target_kp, target_des) = detector.detectAndCompute(target_img["image"], None)
    for comparing_img in imgs:
        (comparing_kp, comparing_des) = detector.detectAndCompute(comparing_img["image"], None)
        try:
            matches = bf.match(target_des, comparing_des)
            dist = [m.distance for m in matches]
            if len(dist) != 0:
                ret = sum(dist) / len(dist)
            else:
                ret = 100000
        except cv2.error:
            ret = 100000

        results.append(
            {
                "target":target_img["filename"],
                "comparing":comparing_img["filename"],
                "ret":ret
            }
        )
        line.append(str(ret))

        print(target_img["filename"], comparing_img["filename"], ret, sum(dist), len(dist))
    outputfile.writelines(",".join(line))
    outputfile.writelines("\n")
#print(results)
outputfile.close()


"""並べ替え"""
#sortfile = open('output/results_sort_test.csv', 'w')
#for s in sorted(results, key=lambda x:x['ret']):
#    if s["ret"] != 0 and s["ret"] != 100000:
#        write_contents = s["target"] + "," + s["comparing"] + "," + str(s["ret"]) + "\n"
#        sortfile.writelines(write_contents)
#sortfile.close()

"""まとめる"""
sortfile = open('output/' + outputfilename + '_sort.txt', 'w')
result_mix = []
for r1 in results:
    for r2 in results:
        if r1["ret"] != 0 and r2["ret"] != 100000:
            if r1["target"] == r2["comparing"] and r1["comparing"] == r2["target"]:
                result_mix.append(
                    {
                        "compare01":r1["target"],
                        "compare02":r1["comparing"],
                        "ret":max(float(r1["ret"]), float(r2["ret"]))
                    }
                )
result_sort_mix = sorted(result_mix, key=lambda x:x['ret'])
namefile = open('names/symbol_name.csv')
lines = namefile.readlines()
for i, rsm in enumerate(result_sort_mix):
    if i%2 == 0:
        symbol1 = lines[int(rsm["compare01"].split(".")[0])].split()[0].split(",")[1]
        symbol2 = lines[int(rsm["compare02"].split(".")[0])].split()[0].split(",")[1]
        print(rsm, symbol1, symbol2)
        write_contents = rsm["compare01"] + "," + rsm["compare02"] + "," + str(rsm["ret"])
        write_contents += ("," + symbol1)
        write_contents += ("," + symbol2 + "\n")
        sortfile.writelines(write_contents)
sortfile.close()
