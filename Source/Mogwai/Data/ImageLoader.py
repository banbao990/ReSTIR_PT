import os
import sys
# print python version
print("Python version:", sys.version)

from falcor import *

assets_folder = "D:/Assets/Falcor"

sceneName = 'VeachAjar'
sceneFile = 'VeachAjar/{}.pyscene'.format(sceneName)
outputDir = '{}/Output/{}'.format(assets_folder, sceneName)
if not os.path.exists(outputDir):
    os.makedirs(outputDir)

refImage = '{}/Refs/VeachAjar.200000.exr'.format(assets_folder)
testImage = '{}/Refs/test.in.exr'.format(assets_folder)


def render_graph():
    g = RenderGraph("ImageLoader")

    loadRenderPassLibrary("ErrorMeasurePass.dll")
    loadRenderPassLibrary("ImageLoader.dll")

    ErrorMeasurePass = createPass('ErrorMeasurePass', {'IgnoreBackground': False,
                                                       'UseLoadedReference': False,  # means off
                                                       'ReferenceImagePath': refImage
                                                       })

    ImageLoader = createPass('ImageLoader', {'filename': testImage})

    g.addPass(ErrorMeasurePass, 'ErrorMeasurePass')
    g.addPass(ImageLoader, 'ImageLoader')

    g.addEdge("ImageLoader.dst", "ErrorMeasurePass.Source")

    g.markOutput("ErrorMeasurePass.Output")

    return g


try:
    m.resizeSwapChain(1280, 720)

    graph = render_graph()
    m.addGraph(graph)
    m.loadScene("{}/{}".format(assets_folder, sceneFile))
except NameError:
    None
