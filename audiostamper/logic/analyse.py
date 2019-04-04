import asyncio
from concurrent.futures import ThreadPoolExecutor

from pydub.utils import mediainfo


async def audio_analyse(file_path):
	executor = ThreadPoolExecutor(max_workers=3)
	loop = asyncio.get_event_loop()
	info = await loop.run_in_executor(executor, mediainfo, file_path)
	return info


async def feature_analyse(file_path):
	def blocks(files, size=65536):
		while True:
			b = files.read(size)
			if not b:
				break
			yield b

	with open(file_path, 'r', encoding='utf-8') as f:
		return dict(
			lines=sum(bl.count('\n') for bl in blocks(f))
		)
