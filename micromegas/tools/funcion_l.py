import subprocess, re
import numpy as np
import pandas as pd

class Likelihood: 
	def __init__(self,data_):
		self.data = data_
		self.ruta = 'data.dat'
		self.rutaG = './main data.dat >temporal.dat'
		self.calc()
		self.omega = self.calc_omega()
		self.mchi2 = self.find_mx2()
		self.like_omega = self.l_omega()
		self.log_like = self.gaussian()
		self.diccionario2 = {'Mchi2':self.mchi2, 'Omega':self.omega}
		self.data.update(self.diccionario2)

	def writer(self,file,dictionary):
		data1=open(file,'w')
		for items in dictionary.items(): 
			data1.write("%s %s\n"%items)
		data1.close()

	def calc(self): 
	    self.writer(self.ruta,self.data) 
	    subprocess.getoutput(self.rutaG)

	def find_command(self, COMMAND):
	    const = 0.0 
	    dato = subprocess.getoutput(COMMAND).strip() 
	    # Elimina espacios en blanco al principio y al final
	    if dato.replace(".", "").replace("e", "").replace("-", "").replace("+", "").isdigit():
	        valor = float(dato)
	        if (valor>=0):
	        	const = valor
	        else:
	        	const = 1e10 
	    else: 
	        const = -1 
	    return const

	def find_mx2(self):
	    COMMAND_MCHI2 = "grep 'Mchi1' temporal.dat | awk 'BEGIN{FS=\" \"};{print $11}' "
	    return self.find_command(COMMAND_MCHI2)

	def calc_omega(self):
		COMMAND_RQ = "grep 'Omega' temporal.dat | awk 'BEGIN{FS=\"=\"};{print $3}'"
		return self.find_command(COMMAND_RQ)

	def l_omega(self):
		omega_th = self.omega
		omega_ex = 0.12
		delta_omega_pdg = ((0.1*omega_th)**2 + 0.001*2)**0.5
		return (omega_th - omega_ex)**2 / delta_omega_pdg**2

	def gaussian(self): 
		return self.l_omega()

	def __str__(self):
		texto=f'Los resultados son'
		for clave, valor in self.data.items():
			texto += '\n'
			texto+=f"{clave} = {valor}"
		return texto

	def get_gaussian(self):
		return self.log_like

	def get_datos(self):
		return self.data 

class Likelihood_two_component:
	def __init__(self,data_):
		self.data = data_
		self.ruta = 'data.dat'
		self.rutaG = './main data.dat >temporal.dat'
		self.calc()
		self.omega = calc_omega
		self.omega1 = self.omega[0]
		self.omega2 = self.omega[1]
		self.mchi2 = self.find_mx2()
		self.like_omega = self.l_omega()
		self.log_like = self.gaussian()
		self.diccionario2 = {'Mchi2':self.mchi2, 'Densidad reliquia':self.omega,'loglikelihood':self.log_like}
		self.data.update(self.diccionario2)

	def writer(self,file,dictionary):
		data1=open(file,'w')
		for items in dictionary.items(): 
			data1.write("%s %s\n"%items)
		data1.close()

	def calc(self): 
	    self.writer(self.ruta,self.data) 
	    subprocess.getoutput(self.rutaG)

	def find_command(self, COMMAND):
	    const = 0.0 
	    dato = subprocess.getoutput(COMMAND).strip() 
	    # Elimina espacios en blanco al principio y al final
	    if dato.replace(".", "").replace("e", "").replace("-", "").replace("+", "").isdigit():
	        valor = float(dato)
	        if (valor>=0):
	        	const = valor
	        else:
	        	const = 1e10 
	    else: 
	        const = -1 
	    return const

	def find_mx2(self):
	    COMMAND_MCHI2 = "grep 'Mchi1' temporal.dat | awk 'BEGIN{FS=\" \"};{print $11}' "
	    return self.find_command(COMMAND_MCHI2)

	def calc_omega(self):
		command = f"grep 'Omega_1h^2' {rute}"
		texto = find_command(command)

		
		texto = texto.replace("=", " ").strip(" ").split()
		omega = [0]*2
		if texto != []:
			omega[0] = float(texto[1])
			omega[1] = float(texto[3])
		else:
			omega[0] = float('inf')
			omega[1] = float('inf')

		return omega

	def l_omega(self):
		omega_th = self.omega1 + self.omega2
		omega_ex = 0.12
		delta_omega_pdg = ((0.1*omega_th)**2 + 0.001*2)**0.5
		return (omega_th - omega_ex)**2 / delta_omega_pdg**2

	def gaussian(self): 
		return self.l_omega()

	def __str__(self):
		texto=f'Los resultados son'
		for clave, valor in self.data.items():
			texto += '\n'
			texto+=f"{clave} = {valor}"
		return texto

	def get_gaussian(self):
		return self.log_like

	def get_datos(self):
		return self.data 


class Likelihood_conPhi:
	def __init__(self,data_):

		#Valores constantes

		self.mh = 125 #GeV
		self.vh = 256 #GeV

		#Cargado de datos
		self.data =  {'MAp':3., 'mphi':1,'Mchi1':0.1,'angle':1e-4,'gX':0.1182,'epsilon':0.1,'ff':0.10}
		 
		self.MAp = data_[0]
		self.mphi = data_[1]
		self.Mchi1 = data_[2]
		self.theta = data_[3]
		self.gX = data_[4]
		self.epsilon = data_[5]
		self.ff = data_[6]
		self.data['MAp'] = self.MAp 
		self.data['mphi'] = self.mphi
		self.data['Mchi1'] = self.Mchi1
		self.data['angle'] = self.theta
		self.data['gX'] = self.gX
		self.data['epsilon'] = self.epsilon
		self.data['ff'] = self.ff
		
		self.vphi = self.MAp / (2*self.gX)
		self.lambda_h, self.lambda_phi, self.lambda_hphi = self.calc_lambda()

		#Direcciones del repositorio
		self.ruta = 'data.dat'
		self.rutaG = './main data.dat >temporal.dat'

		#Funciones
		self.calc()
		self.omega = self.calc_omega()
		self.mchi2 = self.find_mx2()
		self.like_omega = self.l_omega()
		self.log_like = self.gaussian()
		self.diccionario2 = {'Mchi2':self.mchi2, 'Densidad reliquia':self.omega,'loglikelihood':self.log_like}
		self.data.update(self.diccionario2)


	def calc_lambda(self):
	    lambdaH = ((self.mh*np.cos(self.theta))**2 + (self.mphi*np.sin(self.theta))**2)/(2*self.vh**2)
	    lambdaphi = ((self.mh*np.sin(self.theta))**2 + (self.mphi*np.cos(self.theta))**2)/(2*(self.vphi**2))
	    lambdahphi = ((self.mphi**2 - self.mh**2)*np.sin(2*self.theta))/(2*self.vh*self.vphi)
	    return lambdaH, lambdaphi, lambdahphi

	def writer(self,file,dictionary):
		data1=open(file,'w')
		for items in dictionary.items(): 
			data1.write("%s %s\n"%items)
		data1.close()

	def calc(self): 
	    self.writer(self.ruta,self.data) 
	    subprocess.getoutput(self.rutaG)

	def find_command(self, COMMAND):
	    const = 0.0 
	    dato = subprocess.getoutput(COMMAND).strip() 
	    # Elimina espacios en blanco al principio y al final
	    if dato.replace(".", "").replace("e", "").replace("-", "").replace("+", "").isdigit():
	        valor = float(dato)
	        if (valor>=0):
	        	const = valor
	        else:
	        	const = 1e10 
	    else: 
	        const = -1 
	    return const

	def find_mx2(self):
	    COMMAND_MCHI2 = "grep 'Mchi1' temporal.dat | awk 'BEGIN{FS=\" \"};{print $11}' "
	    return self.find_command(COMMAND_MCHI2)

	def calc_omega(self):
		COMMAND_RQ = "grep 'Omega' temporal.dat | awk 'BEGIN{FS=\"=\"};{print $3}'"
		return self.find_command(COMMAND_RQ)

	def l_omega(self):
		omega_th = self.omega
		omega_ex = 0.12
		delta_omega_pdg = ((0.1*omega_th)**2 + 0.001*2)**0.5
		return (omega_th - omega_ex)**2 / delta_omega_pdg**2

	def l_lambda_phi(self):
		lambda_phi_th = self.lambda_phi
		lambda_phi_max = np.sqrt(4*np.pi)
		if lambda_phi_th < lambda_phi_max:
			return 0.0
		else: 
			return float('inf')

	def gaussian(self): 
		like_omega = self.l_omega()
		like_lamnda_phi = self.l_lambda_phi()

		if like_lamnda_phi == float('inf'):
			return float('inf')
		else: 
			return self.l_omega() + self.l_lambda_phi()

	def __str__(self):
		texto=f'Los resultados son'
		for clave, valor in self.data.items():
			texto += '\n'
			texto+=f"{clave} = {valor}"
		return texto

	def get_gaussian(self):
		return self.log_like

	def get_datos(self):
		return self.data 


def extract_annihilation_channels(filename='temporal.dat'):
    """
    Extrae los canales de aniquilación y sus contribuciones porcentuales
    del archivo especificado.
    
    Args:
        filename (str): Nombre del archivo a analizar (por defecto 'temporal.dat')
    
    Returns:
        list: Lista de diccionarios con 'channel' y 'contribution_percentage'
    """
    try:
        with open(filename, 'r') as f:
            content = f.read()
        
        # Buscar la sección de canales después de "Relative contributions"
        pattern = r'Relative contributions in % are displayed((?:\s+\d+%.*)+)'
        match = re.search(pattern, content)
        
        if not match:
            return []
        
        # Extraer todas las líneas con porcentajes
        channels_lines = match.group(1).strip().split('\n')
        channels = []
        
        for line in channels_lines:
            # Buscar el porcentaje y el canal
            line_match = re.search(r'(\d+)%\s+(.+)', line.strip())
            if line_match:
                percentage = int(line_match.group(1))
                channel = line_match.group(2).strip()
                channels.append({
                    'channel': channel,
                    'contribution_percentage': percentage
                })
        
        return channels
        
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {filename}")
        return []
    except Exception as e:
        print(f"Error al extraer canales: {e}")
        return []

class LikelihoodWithChannels:
    def __init__(self, data_):
        self.data = data_
        self.ruta = 'data.dat'
        self.rutaG = './main data.dat > temporal.dat'
        self.calc()
        self.omega = self.calc_omega()
        self.mchi2 = self.find_mx2()
        self.like_omega = self.l_omega()
        self.log_like = self.gaussian()
        
        # Extraer canales de aniquilación
        self.annihilation_channels = extract_annihilation_channels()
        
        self.diccionario2 = {
            'Mchi2': self.mchi2, 
            'Densidad_reliquia': self.omega,
            'loglikelihood': self.log_like,
            'canales_aniquilacion': self.annihilation_channels
        }
        self.data.update(self.diccionario2)
    def writer(self,file,dictionary):
    	data1=open(file,'w')
    	for items in dictionary.items(): 
    		data1.write("%s %s\n"%items)
    	data1.close()
    def calc(self): 
    	self.writer(self.ruta,self.data) 
    	subprocess.getoutput(self.rutaG)
    def find_command(self, COMMAND):
    	const = 0.0 
    	dato = subprocess.getoutput(COMMAND).strip() 
    	# Elimina espacios en blanco al principio y al final
    	if dato.replace(".", "").replace("e", "").replace("-", "").replace("+", "").isdigit():
    		valor = float(dato)
    		if (valor>=0):
    			const = valor
    		else:
    			const = 1e10 
    	else: 
    		const = -1 
    	return const

    def find_mx2(self):
    	COMMAND_MCHI2 = "grep 'Mchi1' temporal.dat | awk 'BEGIN{FS=\" \"};{print $11}' "
    	return self.find_command(COMMAND_MCHI2)


    def calc_omega(self):
    	COMMAND_RQ = "grep 'Omega' temporal.dat | awk 'BEGIN{FS=\"=\"};{print $3}'"
    	return self.find_command(COMMAND_RQ)

    def l_omega(self):
    	omega_th = self.omega
    	omega_ex = 0.12
    	delta_omega_pdg = ((0.1*omega_th)**2 + 0.001*2)**0.5
    	return (omega_th - omega_ex)**2 / delta_omega_pdg**2

    def gaussian(self): 
    	return self.l_omega()

    def __str__(self):
    	texto=f'Los resultados son'
    	for clave, valor in self.data.items():
    		texto += '\n'
    		texto+=f"{clave} = {valor}"
    	return texto

    def get_annihilation_channels(self):
    	"""Devuelve los canales de aniquilación"""
    	return self.annihilation_channels
    
    def get_channels_summary(self):
        """Resumen de los canales"""
        if not self.annihilation_channels:
            return "No se encontraron canales"
        
        summary = "Canales de aniquilación:\n"
        for channel in self.annihilation_channels:
            summary += f"  {channel['contribution_percentage']}%: {channel['channel']}\n"
        
        return summary
    def get_gaussian(self):
    	return self.log_like

    def get_datos(self):
    	return self.data 


if __name__ == '__main__':
	x = [-0.9,1.12,-2,0.01]

	def diccionario(x_):
		data = {'MAp':3., 'mphi':1,'Mchi1':0.1,'angle':1e-4,'gX':0.1182,'epsilon':0.1,'ff':0.10}
		gammap = 0.1 
		alphaD = 0.5
		gx = np.sqrt(4*np.pi*alphaD)
		masa = 10**x_[0]
		masaA = 3*masa 
		lower_bound = 0.7 *(2*masa)
		upper_bound = 1.3 *(2*masa)
		delta = gammap*masa
		f = (gx*delta)/(masaA)
		data['MAp'] = masaA
		data['mphi'] = np.random.uniform(lower_bound, upper_bound)
		data['Mchi1'] = masa
		data['angle'] = 1e-5
		data['gX'] = gx
		data['epsilon'] = 10**x_[1]
		data['ff'] = f
		return data

	def diccionario2():
		data = [0]*7
		gammap = 0.1 
		alphaD = 0.5
		gx = np.sqrt(4*np.pi*alphaD)
		masa = 1e-3
		masaA = 3*masa 
		lower_bound = 0.7 *(2*masa)
		upper_bound = 1.3 *(2*masa)
		delta = gammap*masa
		f = (gx*delta)/(masaA)
		data[0] = masaA
		data[1] = np.random.uniform(lower_bound, upper_bound)
		data[2] = masa
		data[3] = 1e-5
		data[4] = gx
		data[5] = 1e-6
		data[6] = f
		return data

	ob1 = Likelihood(diccionario([1e-4,1e-6]))
	ob2 = Likelihood_conPhi(diccionario2())

	print(ob2)
	#print(ob1)
	#obj = [] 
	#obj.append(ob1.get_datos())
	#print(pd.DataFrame(obj))
	#print(ob1.get_gaussian())
	print(ob2.get_datos())