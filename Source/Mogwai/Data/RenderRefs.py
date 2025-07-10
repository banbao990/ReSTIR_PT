from falcor import *
import os

maxDepth = 10
maxSpp = 200000  # -1 mean infinite
sceneName = 'VeachAjar'
sceneFile = 'VeachAjar/{}.pyscene'.format(sceneName)
outputDir = 'Output/{}'.format(sceneName)
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
    m.loadScene(sceneFile)

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
