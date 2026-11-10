from pathlib import Path
root=Path(__file__).resolve().parents[1]/'public/hardware/servo-fit'
(root/'REPAIR_GUIDE.html').write_text((root/'REPAIR_GUIDE_V3_2.html').read_text(encoding='utf-8'),encoding='utf-8')
print('Published V3.2 repair guide.')
