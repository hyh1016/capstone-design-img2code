from posixpath import abspath
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import time, os, tqdm
from pix2code.model.classes.dataset.Dataset import Dataset
# analysis data using tensorboard
import numpy as np
import matplotlib.pyplot as plt
import numpy as np

# dataPath = "pix2code/datasets/pix2code_datasets/web/all_data"
dataPath = "dataGenerator/data/dsl/"

def getCenterPosition(driver, element):
    location = element.location
    size = element.size
    return (location['x'] + size['width'] / 2, location['y'] + size['height'] / 2)
def gerElementSize(driver, element):
    size = element.size
    return size['width']*size['height']
def plotTagData(path):
    dataset = Dataset()
    dataset.load(dataPath, generate_binary_sequences=True)
    dic = dict()
    for i, tok in enumerate(dataset.next_words):
        if dataset.ids[i] not in dic:
            dic[dataset.ids[i]] = tok.copy()
        else:
            dic[dataset.ids[i]] += tok
        # print(dataset.voc.token_lookup[np.argmax(tok)])
    labelCountMean = np.mean(np.array([v for v in dic.values()]), axis=0)
    print(labelCountMean)
    import matplotlib.pyplot as plt
    plt.barh(list(dataset.voc.token_lookup.values())[::-1], labelCountMean[::-1])
    plt.show()


# 태그별 중심 좌표 분포 출력
def plotCenterPos(path):
    driver = webdriver.Chrome()
    htmls = [f for f in os.listdir(path) if f.endswith('.html')]
    # 태그별 중심 좌표 수집
    centerPosData = dict()
    for i, name in enumerate(htmls):
        html = os.path.join(path, name)
        driver.get(abspath(html))
        time.sleep(0.1)
        
        # retrive center position
        elements = driver.find_elements(By.XPATH, '//*')
        for element in elements:
            center = getCenterPosition(driver, element)
            if center==(0, 0):
                continue
            if element.tag_name not in centerPosData:
                centerPosData[element.tag_name] = [center]
            else:
                centerPosData[element.tag_name].append(center)
    driver.close()

    for tag, pos in centerPosData.items():
        pos = np.array(pos)
        plt.scatter(pos[:, 0], pos[:, 1], label=tag)
    plt.legend()
    plt.show()

    return centerPosData

def plotTagSize(path):
    driver = webdriver.Chrome()
    htmls = [f for f in os.listdir(dataPath) if f.endswith('.html')]
    # 태그별 크기 정보 수집
    sizeData = dict()
    for i, name in enumerate(htmls):
        html = os.path.join(dataPath, name)
        driver.get(abspath(html))
        time.sleep(0.1)
        
        # retrive center position
        elements = driver.find_elements(By.XPATH, '//*')
        for element in elements:
            size = gerElementSize(driver, element)
            if size==(0, 0):
                continue
            if element.tag_name not in sizeData:
                sizeData[element.tag_name] = {size:1}
            else:
                if size not in sizeData[element.tag_name]:
                    sizeData[element.tag_name][size] = 1
                else:
                    sizeData[element.tag_name][size] += 1
    driver.close()

    del(sizeData['html'])
    del(sizeData['style'])
    del(sizeData['body'])
    del(sizeData['main'])
    del(sizeData['nav'])
    print(sizeData)
    # bubble chart


    # x축 : 태그, y축 : 크기, z축 : 개수
    for tag, size in sizeData.items():
        x = [tag]*len(size)
        y = list(size.keys())
        z = list(size.values())
        plt.scatter(x, y, s=z, label=tag)
    # plt.legend()
    plt.show()

    return sizeData


def colorTagPlot(path):
    colors = {'rgba(51, 51, 51, 1)':'black', 'rgba(59, 130, 246, 1)':'blue', 'rgba(245, 245, 245, 1)':'white', 'rgba(249, 115, 22, 1)':'orange', 'rgba(239, 68, 68, 1)':'red', 'rgba(34, 197, 94, 1)':'green'}
    driver = webdriver.Chrome()
    htmls = [f for f in os.listdir(dataPath) if f.endswith('.html')]
    # 태그별 배경 색 정보 수집
    colorData = dict()
    for i, name in enumerate(htmls):
        html = os.path.join(dataPath, name)
        driver.get(abspath(html))
        time.sleep(0.1)
        
        # retrive center position
        elements = driver.find_elements(By.XPATH, '//*')
        for element in elements:
            color = element.value_of_css_property('background-color')
            if color=='rgba(0, 0, 0, 0)':
                continue
            color = colors[color]
            if element.tag_name+color not in colorData:
                colorData[element.tag_name+color] = 1
            else:
                colorData[element.tag_name+color] += 1
        if i==10:
            break
    driver.close()

    # 바 차트
    import matplotlib.pyplot as plt
    import numpy as np

    # x축 : 태그+색, y축 : 개수
    plt.bar(colorData.keys(), colorData.values())
    plt.show()

    return colorData