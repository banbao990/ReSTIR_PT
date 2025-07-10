from falcor import *
import os

refImagePath = '../../../Refs/VeachAjar.195000.exr'


def render_graph_ReSTIRPT():
    g = RenderGraph("ReSTIRPTPass")
    loadRenderPassLibrary("AccumulatePass.dll")
    loadRenderPassLibrary("GBuffer.dll")
    loadRenderPassLibrary("ReSTIRPTPass.dll")
    loadRenderPassLibrary("ToneMapper.dll")
    loadRenderPassLibrary("ScreenSpaceReSTIRPass.dll")
    loadRenderPassLibrary("ErrorMeasurePass.dll")

    ReSTIRGIPlusPass = createPass("ReSTIRPTPass", {'samplesPerPixel': 1, 'enableTemporalReuse': False, 'maxSurfaceBounces': 10})
    g.addPass(ReSTIRGIPlusPass, "ReSTIRPTPass")
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

    g.addEdge("VBufferRT.vbuffer", "ReSTIRPTPass.vbuffer")
    g.addEdge("VBufferRT.mvec", "ReSTIRPTPass.motionVectors")

    g.addEdge("VBufferRT.vbuffer", "ScreenSpaceReSTIRPass.vbuffer")
    g.addEdge("VBufferRT.mvec", "ScreenSpaceReSTIRPass.motionVectors")
    g.addEdge("ScreenSpaceReSTIRPass.color", "ReSTIRPTPass.directLighting")

    g.addEdge("ReSTIRPTPass.color", "AccumulatePass.input")
    g.addEdge("AccumulatePass.output", "ToneMapper.src")

    g.addEdge("AccumulatePass.output", "ErrorMeasurePass.Source")

    g.markOutput("ToneMapper.dst")
    g.markOutput("AccumulatePass.output")
    g.markOutput("ErrorMeasurePass.Output")

    return g


graph_ReSTIRPT = render_graph_ReSTIRPT()

try:
    m.addGraph(graph_ReSTIRPT)
    m.loadScene('VeachAjar/VeachAjar.pyscene')
    m.resizeSwapChain(1280, 720)
except NameError:
    None
