# encoding: utf-8
"""
aggregator.py

Created by Thomas Mangin on 2012-07-14.
Copyright (c) 2009-2013 Exa Networks. All rights reserved.
"""

from exabgp.bgp.message.open.asn import ASN
from exabgp.protocol.ip import IPv4

from exabgp.bgp.message.update.attribute.id import AttributeID
from exabgp.bgp.message.update.attribute import Flag,Attribute


# =============================================================== AGGREGATOR (7)

class Aggregator (Attribute):
	ID = AttributeID.AGGREGATOR
	FLAG = Flag.TRANSITIVE|Flag.OPTIONAL
	MULTIPLE = False
	CACHING = True

	__slots__ = ['asn','speaker','_str']

	def __init__ (self,asn,speaker):
		self.asn = asn
		self.speaker = speaker
		self._str = None

	def pack (self,asn4):
		if asn4:
			return self._attribute(self.asn.pack(True)+self.speaker.pack())
		elif not self.asn.asn4():
			return self._attribute(self.asn.pack(False)+self.speaker.pack())
		else:
			return self._attribute(self.asn.trans()+self.speaker.pack()) + self._attribute(self.asn.pack(True)+self.speaker.pack())

	def __len__ (self):
		raise RuntimeError('size can be 6 or 8 - we can not say - or can we ?')

	def __str__ (self):
		if not self._str:
			self._str = '%s:%s' % (self.asn,self.speaker)
		return self._str

	@classmethod
	def unpack (cls,data,negotiated):
		if negotiated.asn4:
			return cls(ASN.unpack(data[:4]),IPv4.unpack(data[-4:]))
		return cls(ASN.unpack(data[:2]),IPv4.unpack(data[-4:]))

Aggregator.register()

# ============================================================== AGGREGATOR (18)

class Aggregator4 (Aggregator):
	ID = AttributeID.AS4_AGGREGATOR
	__slots__ = ['pack']

	def pack (self,asn4):
		return self._attribute(self.asn.pack(True)+self.speaker.pack())

Aggregator4.register()
