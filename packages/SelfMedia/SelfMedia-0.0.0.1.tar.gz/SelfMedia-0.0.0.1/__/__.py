import json5
import numpy
import torch
import zhconv
import ffmpeg
import whisper
import librosa
import soundfile
import pyloudnorm
import subprocess

import re as regex

from pathlib import Path

from typing import Optional, Union
from pysubs2 import SSAFile, SSAEvent

import xml.etree.ElementTree as ET

import opentimelineio as otio
import opentimelineio.opentime as ot
from opentimelineio.schema import Clip, Timeline, ExternalReference, MissingReference


class ____:
	FPS: int = 16000

	LUFS: float = -15
	TP: float = -0.5

	MAX_GRAN: int = 20000
	MIN_GAP: int = 50

	STEP = 10

	@classmethod
	def genProxy(
		cls,
		rawFiPa: Path, proxyFiPa: Path,
		fps: int = FPS, lufs: float = LUFS, tp: float = TP
	):
		print('<genProxy>')
		pipe = ffmpeg.input(rawFiPa.as_posix())
		pipe = ffmpeg.filter(pipe, "loudnorm", I=lufs, TP=tp)
		pipe = ffmpeg.output(pipe, proxyFiPa.as_posix(), ar=fps, ac=1)
		ffmpeg.run(pipe, quiet=True)
		pass

	@classmethod
	def genDummy(cls, rawFiPa: Path, dummyFiPa: Path):
		print('<genDummy>')
		cmd = ' '.join([
			'ffmpeg -v warning',
			'-f lavfi -i color=c=0x202020:s=1920x1080:r=10',
			'-i "%s"' % rawFiPa.as_posix(),
			'-c:a copy',
			'-shortest',
			'"%s"' % dummyFiPa.as_posix(),
		])
		print(cmd)
		subprocess.run(cmd, encoding='UTF-8')
		pass

	@classmethod
	def getMediaInfo(cls, mediaFiPa: Path):
		pass

	pass
