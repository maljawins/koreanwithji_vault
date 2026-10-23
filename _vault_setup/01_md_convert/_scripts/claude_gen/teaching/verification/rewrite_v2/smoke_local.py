"""Real 12-second media/OCR/Whisper smoke. No credentials, Gemini or workbook writes."""
import importlib.util
from pathlib import Path
import os
import sys

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parents[3] / 'teaching_yt_md_pipeline.py'
spec = importlib.util.spec_from_file_location('teaching_smoke', SCRIPT)
p = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = p
spec.loader.exec_module(p)

os.environ.setdefault('PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK', 'True')
source = HERE.parents[1] / 'YZjWuFVSjjM_27c7dba68cb3/source.mp4'
work = HERE / 'smoke_local'
work.mkdir(exist_ok=True)
video = work / 'source.mp4'
if not video.exists():
    p.run_command(['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-y','-i',str(source),
                   '-t','12','-vf','scale=-2:720','-c:v','libx264','-preset','fast','-crf','24',
                   '-c:a','aac',str(video)])
entry = p.Entry(2,'fixture','05_teaching','12-second smoke','https://youtu.be/YZjWuFVSjjM','X','YZjWuFVSjjM')
p.atomic_json(work/'metadata.json',{'id':entry.vid,'title':entry.title,'channel':entry.channel,'duration':12.})
video, meta = p.download(entry,work,120)
print('720P_MEDIA_OK',meta['duration'],flush=True)
args = p.parse_args(['--max-images','4','--language','en'])
workers = p.PipelineWorkers()
segments = p.transcribe(video,work,args,workers)
print('REAL_WHISPER_OK',len(segments),'segments',flush=True)
frames = p.select_frames(video,work,meta['duration'],args,workers)
print('REAL_OCR_OK',len(frames),'frames',sum(bool(f['ocr']) for f in frames),'with text',flush=True)
timeline = p.build_timeline(segments,frames,meta['duration'])
(work/'timeline.txt').write_text(timeline,encoding='utf-8')
p.atomic_json(work/'smoke_report.json',{'duration':meta['duration'],'segments':len(segments),
    'frame_times':[f['time'] for f in frames],'frames_with_text':sum(bool(f['ocr']) for f in frames),
    'first_audio':segments[0]['text'],'first_ocr':frames[0]['ocr'],
    'paid_calls':0,'scope':'12-second local excerpt, not full-video generation'})
print('LOCAL_SMOKE_PASS; paid calls=0',flush=True)
