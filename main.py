import json
import os
import imageio.v3 as iio

def get_images_data():
    print("**图片数据处理开始**")
    print("-正在打开config.json文件")
    with open('./config.json', 'r', encoding='utf8') as fp:
        config = json.load(fp)
        images_dir = config['images_dir']
        images_data = []
        print("-正在获取文件夹内图片")
        for root, dirs, files in os.walk(images_dir):
            for file in files:
                error_files = []
                print("--正在分析:" + file)
                if ".png" not in file:
                    error_files.append(file)
                    continue

                image_path = "./" + images_dir + "/" + file
                im = iio.immeta(image_path)  # read a standard image

                keywords_array = im['Description'].split(",")
                for index in range(len(keywords_array)):
                    keywords_array[index] = keywords_array[index].lstrip().rstrip()

                comment = json.loads(im['Comment'])
                negative_keywords_array = comment['uc'].split(',')
                for index in range(len(negative_keywords_array)):
                    negative_keywords_array[index] = negative_keywords_array[index].lstrip().rstrip()

                image_url = "./images/" + images_dir + "/" + file
                image_data = {"keywordsArray": keywords_array, "negativeKeywordsArray": negative_keywords_array,
                              "imageUrl": image_url,
                              "seed": comment['seed'], 'r18': config['r18']}
                images_data.append(image_data)
        f = open("./" + config['images_dir'] + ".json", 'w')
        f.write(json.dumps(images_data))
        f.close()

        print("-" + images_dir + ".json 已生成")
        if len(error_files) > 0:
            print("分析失败的文件如下：" + str(error_files))

        print("**图片数据处理完毕**")


get_images_data()
