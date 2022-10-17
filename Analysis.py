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
# dataPath = "dataGenerator/data/dsl/"

def getCenterPosition(driver, element):
    location = element.location
    size = element.size
    return (location['x'] + size['width'] / 2, location['y'] + size['height'] / 2)
def gerElementSize(driver, element):
    size = element.size
    return size['width']*size['height']
def plotTagData(dataPath):
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

def plotTagSize(dataPath):
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


def colorTagPlot(dataPath):
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

def getTokenizedData(path):
    with open(path, 'r') as f:
        a = f.readlines()
    a_token_sequence = []
    for line in a:
        line = line.replace(",", " ,").replace("\n", " \n")
        tokens = line.split(" ")
        for token in tokens:
            a_token_sequence.append(token)
    return a_token_sequence

# 문자열 유사도 계산
from difflib import SequenceMatcher

# 파일 유사도 계산
def fileSimilarity(path1, path2):
    a = getTokenizedData(path1)
    b = getTokenizedData(path2)
    # 배열 유사 리턴
    return SequenceMatcher(None, a, b).ratio()


# get lcs using backtracking
# return correct array
def getLCS(a, b):
    # 2차원 배열 생성
    dp = [[0 for _ in range(len(b)+1)] for _ in range(len(a)+1)]
    # dp[i][j] : a[:i]와 b[:j]의 lcs 길이
    for i in range(1, len(a)+1):
        for j in range(1, len(b)+1):
            if a[i-1]==b[j-1]:
                dp[i][j] = dp[i-1][j-1]+1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    # 해당 문자가 lcs에 포함되는지 확인
    # backtracking
    i, j = len(a), len(b)
    isInLcs = [False for _ in range(len(a))]
    while i>0 and j>0:
        if a[i-1]==b[j-1]:
            isInLcs[i-1] = True
            i -= 1
            j -= 1
        else:
            if dp[i-1][j]>dp[i][j-1]:
                i -= 1
            else:
                j -= 1
    return isInLcs


# 태그별 정답률
def getAccuracyPerTag(path1, path2):
    a_token_sequence = getTokenizedData(path1)
    b_token_sequence = getTokenizedData(path2)
    # lcs
    lcs = getLCS(a_token_sequence, b_token_sequence)
    # 태그별 정답률
    tagAccuracy = dict()
    for i, token in enumerate(a_token_sequence):
        if token not in tagAccuracy:
            # [정답 개수, 전체 개수]
            tagAccuracy[token] = [0, 0]
        if lcs[i]:
            tagAccuracy[token][0] += 1
        tagAccuracy[token][1] += 1
    return tagAccuracy


# 폴더 한번에 유사도 계산
def batchFileSimilarity(path):
    guis = [f for f in os.listdir(path+'dsl/') if f.endswith('.gui')]

    fileAccuracy = []
    tagAccuracy = dict()
    for i, name in enumerate(guis):
        # 파일별 유사도 계산
        path1 = os.path.join(path+'dsl/', name)
        path2 = os.path.join(path+'predicted/', name)
        fileAccuracy.append(fileSimilarity(path1, path2))

        # 태그별 정답률
        tagAccuracyPerFile = getAccuracyPerTag(path1, path2)
        for tag in tagAccuracyPerFile:
            if tag not in tagAccuracy:
                tagAccuracy[tag] = [0, 0]
            tagAccuracy[tag][0] += tagAccuracyPerFile[tag][0]
            tagAccuracy[tag][1] += tagAccuracyPerFile[tag][1]
    return fileAccuracy, tagAccuracy



if __name__ == '__main__':
    fileAccuracy, tagAccuracy = batchFileSimilarity('dataGenerator/data_/')
    print('평균 file accuracy :', sum(fileAccuracy)/len(fileAccuracy))
    plt.bar(tagAccuracy.keys(), [tagAccuracy[tag][0]/tagAccuracy[tag][1] for tag in tagAccuracy])
    plt.show()

