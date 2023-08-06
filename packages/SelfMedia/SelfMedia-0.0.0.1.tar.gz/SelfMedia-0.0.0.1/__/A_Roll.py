from .__ import ____
from .__ import *

from ._AI import VAD, Whisper
from ._Audio import Audio
from ._Texture import Texture


class A_Roll:
	_vad: VAD = None
	_whisp: Whisper = None

	_rawFiPa: Path = None
	_proxyFiPa: Path = None
	_draftFiPa: Path = None
	_proofFiPa: Path = None
	_optimFiPa: Path = None

	_dummyFiPa: Path = None

	_proxy: Audio = None
	_draft: Texture = None
	_proof: Texture = None
	_optim: Texture = None

	def __init__(self, taskDiPa: Path, vad: Optional[VAD], whisp: Optional[Whisper]):
		self._vad = vad
		self._whisp = whisp

		task = taskDiPa.name
		assert taskDiPa.is_dir()
		self._rawFiPa = [_ for _ in taskDiPa.iterdir() if _.stem == task + '┆0_Raw'][0]
		self._proxyFiPa = taskDiPa / (task + '┆1_Proxy.aac')
		self._draftFiPa = taskDiPa / (task + '┆2_Draft.srt')
		self._proofFiPa = taskDiPa / (task + '┆3_Proof.srt')
		self._optimFiPa = taskDiPa / (task + '┆4_Optim.srt')

		self._dummyFiPa = taskDiPa / (task + '┆X_Dummy.mp4')
		pass

	def loadAI(self):
		if not self._vad:
			print('[VAD]')
			self._vad = VAD()
			pass
		if not self._whisp:
			print('[Whisper]')
			self._whisp = Whisper('large')
			pass
		pass

	def genProxy(self):
		if not self._proxyFiPa.is_file():
			____.genProxy(self._rawFiPa, self._proxyFiPa)
			pass
		pass

	def loadProxy(self):
		if not self._proxy:
			self.genProxy()
			self._proxy = Audio.load(self._proxyFiPa).normLufs(____.LUFS)
			pass
		pass

	def genDraft(self):
		if not self._draftFiPa.is_file():
			self.loadProxy()
			self.loadAI()

			cont: Texture = self._vad.probe(self._proxy)
			cont = cont.aggrByGran()

			draft = self._whisp.transcribe(self._proxy, cont)
			draft = draft.calibrate(self._proxy, -60)
			draft = draft.extent([100, 0])
			draft.save(self._draftFiPa.as_posix())
			pass
		pass

	def loadDraft(self):
		if not self._draft:
			self.genDraft()
			self._draft = Texture.load(self._draftFiPa.as_posix())
			pass
		pass

	def loadProof(self):
		if self._proofFiPa.is_file():
			self._proof = Texture.load(self._proofFiPa.as_posix())
			pass
		else:
			print('!!! Proof not exists...')
			pass
		pass

	def genOptim(self, accent: str = None):
		if not self._optimFiPa.is_file():
			self.loadProxy()
			self.loadProof()
			optim = self._proof.calibrate(self._proxy, -50)
			optim = optim.extent([100, 50])
			if accent:
				optim = optim.toAccent(accent)
				pass
			optim.save(self._optimFiPa.as_posix())
			pass
		pass

	def loadOptim(self):
		if not self._optim:
			self.genOptim()
			self._optim = Texture.load(self._optimFiPa.as_posix())
			pass
		pass

	def genDummy(self):
		if not self._dummyFiPa.is_file():
			____.genDummy(self._rawFiPa, self._dummyFiPa)
			pass
		pass

	pass
