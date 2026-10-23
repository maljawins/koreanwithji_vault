"""Conditional Paddle 2 smoke with missing setuptools supplied in-process only.
Does not install packages or fix the base environment. Requires the downloaded
setuptools 79 wheel and the 12-second fixture made by smoke_local.py.
"""
import importlib.util
from pathlib import Path
import sys
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parents[3] / 'teaching_yt_md_pipeline.py'
spec = importlib.util.spec_from_file_location('teaching_base', SCRIPT)
p = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = p
spec.loader.exec_module(p)
work = HERE/'smoke_local'

with tempfile.TemporaryDirectory(prefix='teaching-setuptools-probe-') as directory:
    with zipfile.ZipFile(HERE/'dependency_probe/setuptools-79.0.1-py3-none-any.whl') as archive:
        archive.extractall(directory)
    sys.path.insert(0,directory)
    from setuptools.command.easy_install import easy_install
    workers = p.PipelineWorkers()
    args = p.parse_args(['--language','en'])
    segments,info = workers.get_whisper(args).transcribe(str(work/'audio.wav'),beam_size=5,
        vad_filter=True,condition_on_previous_text=False,language='en')
    transcript = [s.text.strip() for s in segments if s.text.strip()]
    assert transcript
    print('BASE_WHISPER_OK',len(transcript),'segments',flush=True)
    text = p._run_ocr(workers.get_ocr(),work/'frames/001.jpg')
    print('REAL_PADDLE2_OCR',repr(text),flush=True)
    assert '4MAT' in ''.join(text.split()).upper()
    p.atomic_json(work/'base_environment_smoke.json',{'python':sys.executable,
        'ocr_text':text,'transcript':transcript,
        'setuptools':'79.0.1 supplied from temporary extracted wheel; NOT installed',
        'base_environment_still_missing_setuptools':True,'paid_calls':0})
    print('CONDITIONAL_BASE_SMOKE_PASS; installation still required',flush=True)
