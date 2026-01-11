from falcor import *
import os

maxDepth = 10
maxSpp = 200000  # -1 mean infinite
maxSpp = -1

# print python version
import sys
print("Python version:", sys.version)

assets_folder = "D:/Assets/Falcor"

sceneFolder = 'Bistro_v5_2'
sceneName = 'BistroInterior_Wine'
sceneFile = '{}/{}.pyscene'.format(sceneFolder, sceneName)
outputDir = '{}/Output/{}'.format(assets_folder, sceneName)
if not os.path.exists(outputDir):
    os.makedirs(outputDir)


def render_graph_PathTracer():
    g = RenderGraph("MegakernelPathTracer")

    loadRenderPassLibrary("GBuffer.dll")
    loadRenderPassLibrary("MegakernelPathTracer.dll")
    loadRenderPassLibrary("AccumulatePass.dll")
    # loadRenderPassLibrary("ToneMapper.dll")

    VBufferRT = createPass('VBufferRT')
    g.addPass(VBufferRT, 'VBufferRT')
    MegakernelPathTracer = createPass(
        'MegakernelPathTracer',
        {'params': PathTracerParams(maxBounces=maxDepth, maxNonSpecularBounces=maxDepth)}
    )
    g.addPass(MegakernelPathTracer, 'MegakernelPathTracer')
    AccumulatePass = createPass('AccumulatePass')
    g.addPass(AccumulatePass, 'AccumulatePass')
    # ToneMapper = createPass('ToneMapper')
    # g.addPass(ToneMapper, 'ToneMapper')

    g.addEdge('MegakernelPathTracer.color', 'AccumulatePass.input')
    # g.addEdge('AccumulatePass.output', 'ToneMapper.src')
    g.addEdge('VBufferRT.vbuffer', 'MegakernelPathTracer.vbuffer')

    g.markOutput('AccumulatePass.output')
    # g.markOutput('ToneMapper.dst')

    return g


PathTracer = render_graph_PathTracer()

try:
    m.addGraph(PathTracer)
    m.resizeSwapChain(1280, 720)
    m.loadScene("{}/{}".format(assets_folder, sceneFile))

    # m.scene.camera.position = float3(-3.616691,1.087666,-0.418775)
    # m.scene.camera.target = float3(-4.191498,0.940683,-1.223755)
    # m.scene.camera.up = float3(0.000000,1.000000,0.000000)

    if maxSpp > 0:
        m.clock.exitFrame = maxSpp + 1
        m.frameCapture.outputDir = "../../../{}".format(outputDir)
        m.frameCapture.baseFilename = sceneName

        saveInterval = 5000
        frameCount = (maxSpp + saveInterval - 1) // saveInterval
        savedFrames = [i + saveInterval for i in range(0, frameCount * saveInterval, saveInterval)]
        # print(savedFrames)
        m.frameCapture.addFrames(m.activeGraph, savedFrames)

except NameError:
    None
