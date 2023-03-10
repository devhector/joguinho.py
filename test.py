def parser(data):
	method = data.split(" ")[0]
	aux = data.split(" ")[1]
	aux = aux[2:-2]
	data = aux.split("\n")
	return method, data


def main():

	msg = "UPDATE (\n0,120,75,True,8\n1,221,54,False,3\n)"

	method, data = parser(msg)

	print(method)
	print(data)

	print(parser("UPDATE (\n0,11,13,True,8\n)"))

main()