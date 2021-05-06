import sys
import struct

class nn_weight:
	weight_ = []
	bias_ = []
	num_layers_ = 0
	layer_num_ = []

	def load_from_h5_binarized(self, path):
		f = open(path, "rb")
		self.num_layers_ = struct.unpack("i", f.read(4))[0]
		print("num_layers {}".format(self.num_layers_))
		self.layer_num_ = []
		for i in range(0, self.num_layers_):
			num = struct.unpack("i", f.read(4))[0]
			print("num {}".format(num))
			self.layer_num_.append(num)
		for layer in range(0, self.num_layers_-1):
			l0 = self.layer_num_[layer]
			l1 = self.layer_num_[layer+1]
			bb = []
			for i in range(0, l0):
				bb.append(struct.unpack("f", f.read(4))[0])
			ww0 = []
			for i in range(0, l0):
				ww1 = []
				for j in range(0, l1):
					ww1.append(struct.unpack("f", f.read(4))[0])
				ww0.append(ww1)
			weight_.append(ww0)
			bias_.append(bb)
			
			ww = []
			i_last = self.num_layers_ - 1
			for i in range(0, layer_num_[i_last]):
				ww.append(struct.unpack("f", f.read(4))[0])
			self.weight_.append(ww)
		f.close()
		print(self.bias_)
		print(self.weight_)
		
if(__name__ == '__main__'):
	if(len(sys.argv) < 2):
		print("{} <path_h5_binarized>".format(sys.argv[0]))
		sys.exit(0)

	nn = nn_weight()
	nn.load_from_h5_binarized(sys.argv[1])