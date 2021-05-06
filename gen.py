import sys
import struct

class nn_weight:
	weight_ = []
	bias_ = []
	num_layers_ = 0
	layer_num_ = []
	tab_ = "\t"
	float_format_ = "{:.4f}"

	def load_from_h5_binarized(self, path):
		f = open(path, "rb")
		self.num_layers_ = struct.unpack("i", f.read(4))[0]
		#print("num_layers {}".format(self.num_layers_))
		self.layer_num_ = []
		for i in range(0, self.num_layers_):
			num = struct.unpack("i", f.read(4))[0]
			#print("num {}".format(num))
			self.layer_num_.append(num)
		for layer in range(0, self.num_layers_-1):
			l0 = self.layer_num_[layer]
			l1 = self.layer_num_[layer+1]
			#print("l0:{}, l1:{}".format(l0, l1))
			bb = []
			for i in range(0, l1):
				bb.append(struct.unpack("f", f.read(4))[0])
			ww0 = []
			for i in range(0, l0):
				ww1 = []
				for j in range(0, l1):
					ww1.append(struct.unpack("f", f.read(4))[0])
				ww0.append(ww1)
			self.weight_.append(ww0)
			self.bias_.append(bb)

		f.close()
		
	def print_header(self):
		t = self.tab_
		f = self.float_format_
		ss = ""
		for i in range(0, self.num_layers_-1):
			ss += "float bias{}[] = ".format(i) + "{ "
			num = self.layer_num_[i+1]
			for j in range(0, num):
				ss += f.format(self.bias_[i][j]) + ", "
			ss += "};\n"

		for i in range(0, self.num_layers_-1):
			ss += "float weight{}[][{}] = ".format(i, self.layer_num_[self.num_layers_-1]) + "{ "
			for j in range(0, self.layer_num_[i]):
				ss += "{"
				for k in range(0, self.layer_num_[i+1]):
					ss += f.format(self.weight_[i][j][k]) + ", "
				ss += "},"
			ss += "};\n"
		ss += "\n"
		ss += "byte nn(float n0[]){\n"
		for i in range(0, self.num_layers_-1):
			num = self.layer_num_[i+1]
			ss += t+"float n{}[] = ".format(i+1) + "{ "
			for j in range(0, num):
				ss += "0, "
			ss += "};\n"

		for i in range(0, self.num_layers_-1):
			for j in range(0, self.layer_num_[i+1]):
				for k in range(0, self.layer_num_[i]):
					ss += t + "n{}".format(i+1) + "[{}]".format(j) + " += n{}[{}]".format(i, k) + " * weight{}[{}][{}];\n".format(i, k, j)
				ss += t + "n{}[{}] += bias{}[{}];\n".format(i+1, j, i, j) 

		ss += "\n"
		ss += t + "float max_v = -999;\n"
		ss += t + "byte max_idx = 0;\n"
		ss += t + "for(byte i=0;i<{};++i)".format(self.layer_num_[self.num_layers_-1]) + "{\n"
		ss += t+t+ "if(n{}[i] > max_idx)".format(self.num_layers_-1) + "{\n"
		ss += t+t+t+ "max_idx = i;\n"
		ss += t+t+t+ "max_v = n{}[i];\n".format(self.num_layers_-1)
		ss += t+t+ "}\n"
		ss += t + "}\n"
		ss += t + "return max_idx;\n"
		ss += "}\n"
		print(ss)

if(__name__ == '__main__'):
	if(len(sys.argv) < 2):
		print("{} <path_h5_binarized>".format(sys.argv[0]))
		sys.exit(0)

	nn = nn_weight()
	nn.load_from_h5_binarized(sys.argv[1])
	nn.print_header()