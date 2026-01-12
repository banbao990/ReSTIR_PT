import sys
from falcor import *

import torch
print("Torch version:", torch.__version__)

# print python version
print("Python version:", sys.version)

# Configuration
assets_folder = "D:/Assets/Falcor"
sceneName = 'VeachAjar'
sceneFile = 'VeachAjar/{}.pyscene'.format(sceneName)

# Global frame counter for demonstration
g_callback_count = 0


def on_python_callback_from_cpp(frame_count):
    """
    This function is called from C++ every 100 frames from MinimalPathTracer::execute()

    Args:
        frame_count: Current frame number from the renderer
    """
    global g_callback_count
    g_callback_count += 1
    print(f"\n[Python Callback #{g_callback_count}] Called from C++ at frame {frame_count}!")
    print(f"  -> This is a non-blocking callback that doesn't freeze the UI")
    print(f"  -> You can fetch render statistics, update parameters, etc.")
    # Example operations you could do here:
    # - Query render settings
    # - Update shader parameters
    # - Save intermediate results
    # - Trigger analytics
    print()


def render_graph_MinimalPathTracer():
    """Setup the render graph for minimal path tracer"""
    g = RenderGraph("MinimalPathTracer")

    # Load required passes
    loadRenderPassLibrary("AccumulatePass.dll")
    loadRenderPassLibrary("GBuffer.dll")
    loadRenderPassLibrary("MinimalPathTracer.dll")
    loadRenderPassLibrary("ToneMapper.dll")

    # Create passes
    AccumulatePass = createPass("AccumulatePass", {
        'enabled': True,
        'precisionMode': AccumulatePrecision.Single
    })
    g.addPass(AccumulatePass, "AccumulatePass")

    ToneMapper = createPass("ToneMapper", {
        'autoExposure': False,
        'exposureCompensation': 0.0
    })
    g.addPass(ToneMapper, "ToneMapper")

    MinimalPathTracer = createPass("MinimalPathTracer", {
        'mMaxBounces': 3,
        'mComputeDirect': True
    })

    # Register the Python callback with the MinimalPathTracer pass
    print("[Python] Registering Python callback with MinimalPathTracer...")
    MinimalPathTracer.setPythonCallback(on_python_callback_from_cpp)

    g.addPass(MinimalPathTracer, "MinimalPathTracer")

    GBufferRT = createPass("GBufferRT", {
        'samplePattern': SamplePattern.Stratified,
        'sampleCount': 16
    })
    g.addPass(GBufferRT, "GBufferRT")

    # Connect outputs
    g.addEdge("AccumulatePass.output", "ToneMapper.src")
    g.addEdge("GBufferRT.posW", "MinimalPathTracer.posW")
    g.addEdge("GBufferRT.normW", "MinimalPathTracer.normalW")
    g.addEdge("GBufferRT.tangentW", "MinimalPathTracer.tangentW")
    g.addEdge("GBufferRT.faceNormalW", "MinimalPathTracer.faceNormalW")
    g.addEdge("GBufferRT.viewW", "MinimalPathTracer.viewW")
    g.addEdge("GBufferRT.diffuseOpacity", "MinimalPathTracer.mtlDiffOpacity")
    g.addEdge("GBufferRT.specRough", "MinimalPathTracer.mtlSpecRough")
    g.addEdge("GBufferRT.emissive", "MinimalPathTracer.mtlEmissive")
    g.addEdge("GBufferRT.matlExtra", "MinimalPathTracer.mtlParams")
    g.addEdge("MinimalPathTracer.color", "AccumulatePass.input")

    g.markOutput("ToneMapper.dst")
    return g


# Main setup
try:
    print("[Python] Setting up render graph...")
    MinimalPathTracer = render_graph_MinimalPathTracer()
    m.addGraph(MinimalPathTracer)

    print(f"[Python] Loading scene from {assets_folder}/{sceneFile}")
    m.loadScene("{}/{}".format(assets_folder, sceneFile))

    print("[Python] Resizing swap chain to 1280x720")
    m.resizeSwapChain(1280, 720)

    print("[Python] Setup complete! The render will continue in the background.")
    print("[Python] Every 100 frames, MinimalPathTracer will call on_python_callback_from_cpp()")
    print("[Python] The UI will remain responsive and you can interact with the window.")
    print("[Python] Press ESC or close the window to exit.")
    print()

except NameError as e:
    print(f"[Python] NameError (this may be expected if running without Mogwai): {e}")
except AttributeError as e:
    print(f"[Python] AttributeError: {e}")
    print("[Python] Make sure the C++ code has been rebuilt with Python callback support.")
except Exception as e:
    print(f"[Python] Error during setup: {e}")

# Note: Do NOT use a for loop with m.renderFrame() here!
# The render loop is handled internally by Falcor/Mogwai.
# The Python callback on_python_callback_from_cpp() will be called from C++ every 100 frames.
