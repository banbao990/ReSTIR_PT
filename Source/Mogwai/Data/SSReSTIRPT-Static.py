from falcor import *
import os

assets_folder = "D:/Assets/Falcor"

sceneFolder = 'Bistro_v5_2'
sceneName = 'BistroInterior_Wine'
sceneFile = '{}/{}.pyscene'.format(sceneFolder, sceneName)
outputDir = '{}/Output/{}'.format(assets_folder, sceneName)
if not os.path.exists(outputDir):
    os.makedirs(outputDir)

refImagePath = '../../../Refs/{}.195000.exr'.format(sceneName)

def render_graph_ReSTIRPT():
    g = RenderGraph("SS-ReSTIRPTPass")
    loadRenderPassLibrary("AccumulatePass.dll")
    loadRenderPassLibrary("GBuffer.dll")
    loadRenderPassLibrary("ToneMapper.dll")
    loadRenderPassLibrary("ScreenSpaceReSTIRPass.dll")
    loadRenderPassLibrary("ErrorMeasurePass.dll")

    VBufferRT = createPass("VBufferRT", {'samplePattern': SamplePattern.Center, 'sampleCount': 1, 'texLOD': TexLODMode.Mip0, 'useAlphaTest': True})
    g.addPass(VBufferRT, "VBufferRT")
    AccumulatePass = createPass("AccumulatePass", {'enableAccumulation': False, 'precisionMode': AccumulatePrecision.Double})
    g.addPass(AccumulatePass, "AccumulatePass")
    ToneMapper = createPass("ToneMapper", {'autoExposure': False, 'exposureCompensation': 0.0, 'operator': ToneMapOp.Linear})
    g.addPass(ToneMapper, "ToneMapper")
    ScreenSpaceReSTIRPass = createPass("ScreenSpaceReSTIRPass")
    g.addPass(ScreenSpaceReSTIRPass, "ScreenSpaceReSTIRPass")
    ErrorMeasurePass = createPass('ErrorMeasurePass', {'ReferenceImagePath': refImagePath, 'IgnoreBackground': False,
                                                       'UseLoadedReference': False  # means off
                                                       })
    g.addPass(ErrorMeasurePass, 'ErrorMeasurePass')

    g.addEdge("VBufferRT.vbuffer", "ScreenSpaceReSTIRPass.vbuffer")
    g.addEdge("VBufferRT.mvec", "ScreenSpaceReSTIRPass.motionVectors")
    g.addEdge("ScreenSpaceReSTIRPass.color", "AccumulatePass.input")
    g.addEdge("AccumulatePass.output", "ToneMapper.src")

    g.addEdge("AccumulatePass.output", "ErrorMeasurePass.Source")

    g.markOutput("ToneMapper.dst")
    g.markOutput("AccumulatePass.output")
    g.markOutput("ErrorMeasurePass.Output")

    return g


graph_ReSTIRPT = render_graph_ReSTIRPT()

try:
    m.addGraph(graph_ReSTIRPT)
    m.loadScene("{}/{}".format(assets_folder, sceneFile))
    m.resizeSwapChain(1280, 720)
except NameError:
    None
