import streamlit as st

st.markdown(
    '<div class="page-title">How it works</div>'
    '<div class="page-sub">A look behind the scenes: from your photo to a diagnosis.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="steps">'
    '<div class="step"><div class="num">1</div><div class="ft">Capture</div>'
    '<div class="fd">You upload or take a photo of a leaf in the browser.</div></div>'
    '<div class="step"><div class="num">2</div><div class="ft">Send</div>'
    '<div class="fd">Streamlit sends the image to the FastAPI backend.</div></div>'
    '<div class="step"><div class="num">3</div><div class="ft">Preprocess</div>'
    '<div class="fd">The image is resized to 224 × 224 and colour-normalised.</div></div>'
    '<div class="step"><div class="num">4</div><div class="ft">Predict</div>'
    '<div class="fd">EfficientNetV2-S scores all 27 classes. Softmax turns scores into probabilities.</div></div>'
    '<div class="step"><div class="num">5</div><div class="ft">Explain</div>'
    '<div class="fd">The top result, top-3 list and advice are sent back and displayed.</div></div>'
    "</div>",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-head">The model</div>'
    '<div class="kv">'
    '<div class="kv-row"><span>Architecture</span><b>EfficientNetV2-S (ImageNet pre-trained)</b></div>'
    '<div class="kv-row"><span>Framework</span><b>PyTorch</b></div>'
    '<div class="kv-row"><span>Input</span><b>224 × 224 RGB</b></div>'
    '<div class="kv-row"><span>Training data</span><b>PlantVillage · 6 crops · 27 classes</b></div>'
    '<div class="kv-row"><span>Optimiser</span><b>AdamW + OneCycle learning rate</b></div>'
    '<div class="kv-row"><span>Regularisation</span><b>Label smoothing, heavy augmentation</b></div>'
    '<div class="kv-row"><span>Training hardware</span><b>Google Colab GPU, mixed precision</b></div>'
    '<div class="kv-row"><span>Serving</span><b>FastAPI (CPU inference)</b></div>'
    '<div class="kv-row"><span>Interface</span><b>Streamlit</b></div>'
    "</div>",
    unsafe_allow_html=True,
)

st.markdown('<div class="section-head">Taking a good photo</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="grid-2">'
    '<div class="card"><div class="tip-title ok">✓ Do</div><ul class="tip-list">'
    "<li>Photograph a single leaf, filling most of the frame</li>"
    "<li>Use natural daylight</li>"
    "<li>Keep the affected area sharp and in focus</li>"
    "<li>Use a plain background if you can</li></ul></div>"
    '<div class="card"><div class="tip-title bad">✗ Avoid</div><ul class="tip-list">'
    "<li>Blurry or very dark photos</li>"
    "<li>Many leaves or a whole field in one shot</li>"
    "<li>Heavy filters or strong shadows</li>"
    "<li>Photos of fruit, stems or crops not in the library</li></ul></div>"
    "</div>",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-head">Limitations</div>'
    '<div class="card"><ul class="tip-list">'
    "<li>The model only knows 6 crops and 27 classes. Any other plant will still get an answer, but it will be wrong.</li>"
    "<li>It was trained on PlantVillage, whose photos are mostly taken on plain backgrounds. "
    "Accuracy on busy field photos can be lower, so check the confidence score.</li>"
    "<li>Results under 60% confidence are marked <b>Not sure</b>.</li>"
    "<li>This is a screening tool, not a replacement for an agronomist.</li></ul></div>",
    unsafe_allow_html=True,
)
