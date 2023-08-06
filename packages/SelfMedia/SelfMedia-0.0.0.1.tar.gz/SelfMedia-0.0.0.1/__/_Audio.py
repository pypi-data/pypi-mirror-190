from .__ import ____
from .__ import *

from ._Stamp import Stamp


class Audio:
	sig: numpy.ndarray = None
	fps: int = None

	def __init__(self, sig: numpy.ndarray, fps: int):
		self.sig = sig.copy()
		self.fps = fps
		pass

	@classmethod
	def load(cls, mediaFiPa: Path, fps: int = ____.FPS):
		print('<load>')
		sig, fps = librosa.load(mediaFiPa.as_posix(), sr=fps)
		return cls(sig, fps)

	def __getitem__(self, stamp: Stamp):
		fStamp = [round(_ / 1000 * self.fps) for _ in stamp]
		return Audio(self.sig[slice(*fStamp)], self.fps)

	def pick(self, event: SSAEvent):
		return self[Stamp(event.start, event.end)]

	def dura(self):
		return round(len(self.sig) / self.fps * 1000)

	def save(self, oFiPa: Path) -> None:
		soundfile.write(oFiPa, self.sig, self.fps)
		pass

	def trim(self, db: float):
		_, fStamp = librosa.effects.trim(
			self.sig,
			top_db=-db,
			ref=1,
			frame_length=256,
			hop_length=64,
		)
		audio = Audio(_, self.fps)
		stamp = Stamp(*fStamp, unit=self.fps)
		return audio, stamp

	def pad(self, targDura: int = 20000):
		targLen = round(targDura / 1000 * self.fps)
		padLen = max(0, targLen - len(self.sig))
		sig = numpy.pad(self.sig, (0, padLen))
		return Audio(sig, self.fps)

	def normPeak(self, peak: float = -1):
		print('<normPeak>')
		sig = pyloudnorm.normalize.peak(self.sig, peak)
		return Audio(sig, self.fps)

	def normLufs(self, lufs: float = -15):
		print('<normLufs>')
		curr = pyloudnorm.Meter(self.fps).integrated_loudness(self.sig)
		sig = pyloudnorm.normalize.loudness(self.sig, curr, lufs)
		return Audio(sig, self.fps)

	pass
