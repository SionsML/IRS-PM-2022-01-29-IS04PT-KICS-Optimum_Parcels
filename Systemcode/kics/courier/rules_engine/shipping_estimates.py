import pandas as pd
import inspect
import os
import math

import warnings
warnings.filterwarnings("ignore", "This pattern is interpreted as a regular expression, and has match groups. To actually get the groups, use str.extract.")

def get_fedex_estimates(data_assets_relpath, dest_country, weight, dim_given=False, dim_lwh=None):
	
	fedex_estimates = []

	if dest_country != "Singapore":
	
		try:
			fedex_data_relpath = os.path.join(data_assets_relpath, "FedEx Rates and Zones.xlsx")
			print(fedex_data_relpath)
			rates_df = pd.read_excel(fedex_data_relpath, "Shipment Rates", engine="openpyxl")
			rates_kg_df = pd.read_excel(fedex_data_relpath, "Shipment Rates per kg", engine="openpyxl")
			zones_df = pd.read_excel(fedex_data_relpath, "FedEx SG - Zone Index", engine="openpyxl")
			times_df = pd.read_excel(fedex_data_relpath, "Estimated Transit Times", engine="openpyxl")
		except:
			print("ERROR READING DATA EXCEL FILES!")
			return fedex_estimates
		
		other_remarks = "All rates are exclusive of all applicable tax. For special fees and fuel surcharge, please refer to the Surcharge and Other Information page for details."
		applicable_services = ["IPE", "IP", "IE", "IF", "IPF", "IEF"]
		length_lim = 274
		lengir_lim = 330
		length = None
		lengir = None
		dim_weight = 0
		
		if dim_given:
			dim_lwh = sorted(dim_lwh, reverse=True)
			length = dim_lwh[0]
			width = dim_lwh[1]
			height = dim_lwh[2]
			girth = 2*(width + height)
			lengir = length + girth

			dim_weight = (length * width * height) / 5000    # Find dimensional weight
			
		if weight > dim_weight:
			dim_weight = weight    # Use higher of weight and dimensional weight
			
		if dim_weight < 21:
			dim_weight = math.ceil(dim_weight * 2.0) / 2.0   # Round up to nearest 0.5kg
		else:
			dim_weight = math.ceil(dim_weight)    # Round up to nearest 1kg
		
		if dim_weight <= 68:
			if dim_given:
				if ((length <= length_lim) and (lengir <= lengir_lim)):
					applicable_services = ["IPE", "IP", "IE", "IF"]
				else:
					applicable_services = ["IE"]
			else:
				applicable_services = ["IPE", "IP", "IE", "IF"]
		else:
			applicable_services = ["IPF", "IEF"]
			
		dest_zone_dict = zones_df[zones_df["Territory"]==dest_country].iloc[0].to_dict()
		dest_zone_dict = {k:v for k, v in dest_zone_dict.items() if k != "Territory"}
		
		for svc, zone in dest_zone_dict.items():
			if ((svc in applicable_services) and (not pd.isna(zone))):
				
				earliest_transit = times_df[times_df["Service"]==svc]["Earliest Time (days)"].iloc[0]
				latest_transit = times_df[times_df["Service"]==svc]["Latest Time (days)"].iloc[0]
				
				rates_df_svc_filter = rates_df["Rates in SGD"].str.contains(f"({svc})")
				rates_df_lower_lim_filter = rates_df["Lower Limit (kg) (Exclusive)"] < dim_weight
				rates_df_upper_lim_filter = rates_df["Upper Limit (kg) (Inclusive)"] >= dim_weight
				
				temp_df = rates_df[(rates_df_svc_filter) & (rates_df_lower_lim_filter) & (rates_df_upper_lim_filter)][["Rates in SGD", zone]]
				
				for i, row in temp_df.iterrows():
					fedex_estimates.append({"Service Provider" : "FedEx",
											"Service" : row["Rates in SGD"],
											"Estimated Rate" : round(row[zone], 2),
											"Estimated Transit Time" : (earliest_transit, latest_transit),
											"Other Remarks" : other_remarks,
											"Insurance" : "Yes",
											"Re Delivery" : 3,
											"Home Pick Up" : "Yes"
										   }
										  )
					
				rates_kg_df_svc_filter = rates_kg_df["Rates (per kg) in SGD"].str.contains(f"({svc})")
				rates_kg_df_lower_lim_filter = rates_kg_df["Lower Limit (kg) (Inclusive)"] <= dim_weight
				rates_kg_df_upper_lim_filter = rates_kg_df["Upper Limit (kg) (Inclusive)"] >= dim_weight
				
				temp_df = rates_kg_df[(rates_kg_df_svc_filter) & (rates_kg_df_lower_lim_filter) & (rates_kg_df_upper_lim_filter)][["Rates (per kg) in SGD", zone]]
				
				for i, row in temp_df.iterrows():
					fedex_estimates.append({"Service Provider" : "FedEx",
											"Service" : row["Rates (per kg) in SGD"],
											"Estimated Rate" : round(row[zone] * dim_weight, 2),
											"Estimated Transit Time" : (earliest_transit, latest_transit),
											"Other Remarks" : other_remarks,
											"Insurance" : "Yes",
											"Re Delivery" : 3,
											"Home Pick Up" : "Yes"
										   }
										  )
				
	return fedex_estimates

def get_ups_estimates(data_assets_relpath, dest_country, weight, dim_given=False, dim_lwh=None):
	
	ups_estimates = []
	
	if dest_country == "Singapore":

		try:
			ups_data_relpath = os.path.join(data_assets_relpath, "UPS Rates and Zones.xlsx")
			dom_rates_df = pd.read_excel(ups_data_relpath, "Domestic Rates", engine="openpyxl")
			times_df = pd.read_excel(ups_data_relpath, "Estimated Transit Times", engine="openpyxl")
		except:
			print("ERROR READING DATA EXCEL FILES!")
			return ups_estimates
		
		applicable_services = ["UPS Express Saver - Domestic"]
		length_lim = 274
		lengir_lim = 400
		length = None
		lengir = None
		dim_weight = 0
		
		if dim_given:
			dim_lwh = sorted(dim_lwh, reverse=True)
			length = dim_lwh[0]
			width = dim_lwh[1]
			height = dim_lwh[2]
			girth = 2*(width + height)
			lengir = length + girth

			dim_weight = (length * width * height) / 5000    # Find dimensional weight

		if weight > dim_weight:
			dim_weight = weight    # Use higher of weight and dimensional weight

		if dim_weight < 21:
			dim_weight = math.ceil(dim_weight * 2.0) / 2.0   # Round up to nearest 0.5kg
		else:
			dim_weight = math.ceil(dim_weight)    # Round up to nearest 1kg

		if dim_weight <= 70:
			if dim_given:
				if ((length <= length_lim) and (lengir <= lengir_lim)):
					applicable_services = ["UPS Express Saver - Domestic"]
				else:
					applicable_services = []
			else:
				applicable_services = ["UPS Express Saver - Domestic"]
		else:
			applicable_services = []
		
		for svc in applicable_services:
			
			earliest_transit = times_df[times_df["Service"]==svc]["Earliest Time (days)"].iloc[0]
			latest_transit = times_df[times_df["Service"]==svc]["Latest Time (days)"].iloc[0]
			
			dom_rates_df_svc_filter = dom_rates_df["UPS Service"].str.contains(f"({svc})")
			dom_rates_df_lower_lim_filter = dom_rates_df["Min Weight (kg) (Exclusive)"] < dim_weight
			dom_rates_df_upper_lim_filter = dom_rates_df["Max Weight (kg) (Inclusive)"] >= dim_weight

			temp_df = dom_rates_df[(dom_rates_df_svc_filter) & (dom_rates_df_lower_lim_filter) & (dom_rates_df_upper_lim_filter)]

			for i, row in temp_df.iterrows():
				
				ups_estimates.append({"Service Provider" : "UPS",
									  "Service" : svc,
									  "Estimated Rate" : round(row["Rate in SGD"], 2),
									  "Estimated Transit Time" : (earliest_transit, latest_transit),
									  "Other Remarks" : "",
									  "Insurance" : "Yes",
									  "Re Delivery" : 2,
									  "Home Pick Up" : "Yes"
									 }
									)
	
	else:
		try:
			ups_data_relpath = os.path.join(data_assets_relpath, "UPS Rates and Zones.xlsx")
			intl_rates_df = pd.read_excel(ups_data_relpath, "International Rates", engine="openpyxl")
			zones_df = pd.read_excel(ups_data_relpath, "Zone Index", engine="openpyxl")
			times_df = pd.read_excel(ups_data_relpath, "Estimated Transit Times", engine="openpyxl")
		except:
			print("ERROR READING DATA EXCEL FILES!")
			return ups_estimates
		
		intl_rates_df["Remarks"].fillna("", inplace=True)

		applicable_services = ["UPS Worldwide Express Plus", "UPS Worldwide Express", "UPS Worldwide Express Saver", "UPS Worldwide Expedited"]
		length_lim = 274
		lengir_lim = 400
		length = None
		lengir = None
		dim_weight = 0
		
		if dim_given:
			dim_lwh = sorted(dim_lwh, reverse=True)
			length = dim_lwh[0]
			width = dim_lwh[1]
			height = dim_lwh[2]
			girth = 2*(width + height)
			lengir = length + girth

			dim_weight = (length * width * height) / 5000    # Find dimensional weight

		if weight > dim_weight:
			dim_weight = weight    # Use higher of weight and dimensional weight

		if dim_weight < 21:
			dim_weight = math.ceil(dim_weight * 2.0) / 2.0   # Round up to nearest 0.5kg
		else:
			dim_weight = math.ceil(dim_weight)    # Round up to nearest 1kg

		if dim_weight <= 70:
			if dim_given:
				if ((length <= length_lim) and (lengir <= lengir_lim)):
					applicable_services = ["UPS Worldwide Express Plus", "UPS Worldwide Express", "UPS Worldwide Express Saver", "UPS Worldwide Expedited"]
				else:
					applicable_services = []
			else:
				applicable_services = ["UPS Worldwide Express Plus", "UPS Worldwide Express", "UPS Worldwide Express Saver", "UPS Worldwide Expedited"]
		else:
			applicable_services = []
			
		dest_zone_dict = zones_df[zones_df["Territory"]==dest_country].iloc[0].to_dict()
		dest_zone_dict = {k:v for k, v in dest_zone_dict.items() if k != "Territory"}
		
		for svc, zone in dest_zone_dict.items():
			if ((svc in applicable_services) and (not pd.isna(zone))):

				earliest_transit = times_df[times_df["Service"]==svc]["Earliest Time (days)"].iloc[0]
				latest_transit = times_df[times_df["Service"]==svc]["Latest Time (days)"].iloc[0]
				
				svc_copy = svc
				if svc == "UPS Worldwide Express Plus":
					svc_copy = "UPS Worldwide Express"

				intl_rates_df_svc_filter = intl_rates_df["UPS Service"] == svc_copy
				intl_rates_df_lower_lim_filter = intl_rates_df["Lower Limit (kg) (Exclusive)"] < dim_weight
				intl_rates_df_upper_lim_filter = intl_rates_df["Upper Limit (kg) (Inclusive)"] >= dim_weight

				temp_df = intl_rates_df[(intl_rates_df_svc_filter) & (intl_rates_df_lower_lim_filter) & (intl_rates_df_upper_lim_filter)]

				for i, row in temp_df.iterrows():
					
					if svc == "UPS Worldwide Express Plus":
						rate = round(row[zone] + 73, 2)
					else:
						rate = round(row[zone], 2)
					
					ups_estimates.append({"Service Provider" : "UPS",
										  "Service" : svc,
										  "Estimated Rate" : rate,
										  "Estimated Transit Time" : (earliest_transit, latest_transit),
										  "Other Remarks" : row["Remarks"],
										  "Insurance" : "Yes",
										  "Re Delivery" : 2,
										  "Home Pick Up" : "Yes"
										 }
										)
					
	return ups_estimates

def get_dhl_estimates(data_assets_relpath, dest_country, weight, dim_given=False, dim_lwh=None):
	
	dhl_estimates = []
	
	if dest_country != "Singapore":
		
		try:
			dhl_data_relpath = os.path.join(data_assets_relpath, "DHL Rates and Zones.xlsx")
			rates_df = pd.read_excel(dhl_data_relpath, "Shipment Rates - DHL Express WW", engine="openpyxl")
			zones_df = pd.read_excel(dhl_data_relpath, "Zone Index", engine="openpyxl")
		except:
			print("ERROR READING DATA EXCEL FILES!")
			return dhl_estimates

		rates_df["Remarks"].fillna("", inplace=True)
		
		applicable_services = ["DHL Express Worldwide", "DHL Express 12:00", "DHL Express 9:00"]

		if ((weight > 30) and (weight <= 70)):
			applicable_services = ["DHL Express Worldwide", "DHL Express 12:00"]
		elif weight > 70:
			applicable_services = []
			return dhl_estimates

		if dim_given:
			dim_lwh = sorted(dim_lwh, reverse=True)
			length = dim_lwh[0]
			width = dim_lwh[1]
			height = dim_lwh[2]

			if ((length > 120) or (width > 80) or (height > 80)):
				return dhl_estimates

		dest_zone_dict = zones_df[zones_df["Territory"]==dest_country].iloc[0].to_dict()
		dest_zone_dict = {k:v for k, v in dest_zone_dict.items() if k != "Territory"}

		for svc, zone in dest_zone_dict.items():
			if ((svc in applicable_services) and (not pd.isna(zone))):

				is_doc = False
				if zone == "doc":
					is_doc = True
					zone = dest_zone_dict["DHL Express Worldwide"]

				rates_df_doc_filter = rates_df["Documents / Everything"] == "Documents"
				rates_df_lower_lim_filter = rates_df["Lower Limit (kg) (Exclusive)"] < weight
				rates_df_upper_lim_filter = rates_df["Upper Limit (kg) (Inclusive)"] >= weight

				if is_doc:
					temp_df = rates_df[(rates_df_lower_lim_filter) & (rates_df_upper_lim_filter) & (rates_df_doc_filter)]
				else:
					temp_df = rates_df[(rates_df_lower_lim_filter) & (rates_df_upper_lim_filter)]

				for i, row in temp_df.iterrows():

					if svc == "DHL Express Worldwide":
						rate = round(row[zone], 2)
						earliest_transit = 1
						latest_transit = 2
						insurance = "No"
					elif svc == "DHL Express 12:00":
						rate = round(row[zone] + 20, 2)
						earliest_transit = 1
						latest_transit = 1 
						insurance = "Yes"
					elif svc == "DHL Express 9:00":
						rate = round(row[zone] + 40, 2)
						earliest_transit = 1
						latest_transit = 1 
						insurance = "Yes"

					dhl_estimates.append({"Service Provider" : "DHL",
										  "Service" : svc,
										  "Estimated Rate" : rate,
										  "Estimated Transit Time" : (earliest_transit, latest_transit),
										  "Other Remarks" : row["Remarks"],
										  "Insurance" : insurance,
										  "Re Delivery" : 2,
										  "Home Pick Up" : "No"
										 }
										)
	
	return dhl_estimates

def get_singpost_estimates(data_assets_relpath, dest_country, weight, dim_given=False, dim_lwh=None):
	
	singpost_estimates = []
	
	if dest_country == "Singapore":
		
		try:
			singpost_data_relpath = os.path.join(data_assets_relpath, "SingPost Rates and Zones.xlsx")
			dom_rates_df = pd.read_excel(singpost_data_relpath, "Domestic Rates", engine="openpyxl")
			times_df = pd.read_excel(singpost_data_relpath, "Estimated Transit Times", engine="openpyxl")
		except:
			print("ERROR READING DATA EXCEL FILES!")
			return singpost_estimates
		
		dom_rates_df["Max L (cm)"].fillna(500, inplace=True)
		dom_rates_df["Max W (cm)"].fillna(500, inplace=True)
		dom_rates_df["Max H (cm)"].fillna(500, inplace=True)
		dom_rates_df["Max L+2W+2H (cm)"].fillna(5000, inplace=True)
		dom_rates_df["Remarks"].fillna("", inplace=True)
		times_df = times_df[times_df["Domestic or International"] == "Domestic"]
		
		dom_rates_df_lower_lim_filter = dom_rates_df["Min Weight (kg) (Exclusive)"] < weight
		dom_rates_df_upper_lim_filter = dom_rates_df["Max Weight (kg) (Inclusive)"] >= weight
		
		filtered_dom_rates_df = dom_rates_df[(dom_rates_df_lower_lim_filter) & (dom_rates_df_upper_lim_filter)]
		
		if dim_given:
			dim_lwh = sorted(dim_lwh, reverse=True)
			length = dim_lwh[0]
			width = dim_lwh[1]
			height = dim_lwh[2]
			girth = 2*(width + height)
			lengir = length + girth
			
			dom_rates_df_max_l_filter = filtered_dom_rates_df["Max L (cm)"] >= length
			dom_rates_df_max_w_filter = filtered_dom_rates_df["Max W (cm)"] >= width
			dom_rates_df_max_h_filter = filtered_dom_rates_df["Max H (cm)"] >= height
			dom_rates_df_max_lengir_filter = filtered_dom_rates_df["Max L+2W+2H (cm)"] >= lengir
			
			filtered_dom_rates_df = filtered_dom_rates_df[(dom_rates_df_max_l_filter) &
														  (dom_rates_df_max_w_filter) &
														  (dom_rates_df_max_h_filter) &
														  (dom_rates_df_max_lengir_filter)
														 ]
		
		for i, row in filtered_dom_rates_df.iterrows():
			
			transit_times_filter = times_df["Service"].apply(lambda s: True if s in row["SingPost Service"] else False)
			earliest_transit = times_df[transit_times_filter].iloc[0]["Earliest Time (days)"]
			if earliest_transit != 0.08:
				earliest_transit = int(earliest_transit)
			latest_transit = times_df[transit_times_filter].iloc[0]["Latest Time (days)"]
			insurance = times_df[transit_times_filter].iloc[0]["Insurance"]
			home_pick_up = times_df[transit_times_filter].iloc[0]["Home Pick Up"]
			
			singpost_estimates.append({"Service Provider" : "SingPost",
									   "Service" : row["SingPost Service"],
									   "Estimated Rate" : round(row["Rate in SGD"], 2),
									   "Estimated Transit Time" : (earliest_transit, latest_transit),
									   "Other Remarks" : row["Remarks"],
									   "Insurance" : insurance,
									   "Re Delivery" : 2,
									   "Home Pick Up" : home_pick_up
									  }
									 )

	else:
		try:
			singpost_data_relpath = os.path.join(data_assets_relpath, "SingPost Rates and Zones.xlsx")
			intl_rates_df = pd.read_excel(singpost_data_relpath, "International Rates", engine="openpyxl")
			zones_df = pd.read_excel(singpost_data_relpath, "Zone Index", engine="openpyxl")
			times_df = pd.read_excel(singpost_data_relpath, "Estimated Transit Times", engine="openpyxl")
		except:
			print("ERROR READING DATA EXCEL FILES!")
			return singpost_estimates
		
		intl_rates_df["Max L (cm)"].fillna(500, inplace=True)
		intl_rates_df["Max W (cm)"].fillna(500, inplace=True)
		intl_rates_df["Max H (cm)"].fillna(500, inplace=True)
		intl_rates_df["Max L+W+H (cm)"].fillna(5000, inplace=True)
		intl_rates_df["Max L+2W+2H (cm)"].fillna(5000, inplace=True)
		intl_rates_df["Remarks"].fillna("", inplace=True)
		times_df = times_df[times_df["Domestic or International"] == "International"]
		
		dest_zone_dict = zones_df[zones_df["Territory"]==dest_country].iloc[0].to_dict()
		dest_zone_dict = {k:v for k, v in dest_zone_dict.items() if k != "Territory"}
		dest_zone_dict = {(k):(int(v) if ((type(v)==float) and (not pd.isna(v))) else v) for k, v in dest_zone_dict.items()}

		for svc, zone in dest_zone_dict.items():
			if not pd.isna(zone):

				intl_rates_df_zone_filter = intl_rates_df["Zone"] == zone
				intl_rates_df_svc_filter = intl_rates_df["SingPost Service"].str.contains(svc)
				intl_rates_df_lower_lim_filter = intl_rates_df["Min Weight (kg) (Exclusive)"] < weight
				intl_rates_df_upper_lim_filter = intl_rates_df["Max Weight (kg) (Inclusive)"] >= weight

				temp_df = intl_rates_df[(intl_rates_df_zone_filter) &
										(intl_rates_df_svc_filter) &
										(intl_rates_df_lower_lim_filter) &
										(intl_rates_df_upper_lim_filter)
									   ]

				if dim_given:
					dim_lwh = sorted(dim_lwh, reverse=True)
					length = dim_lwh[0]
					width = dim_lwh[1]
					height = dim_lwh[2]
					lenwidhei = length + width + height
					girth = 2*(width + height)
					lengir = length + girth

					intl_rates_df_max_l_filter = temp_df["Max L (cm)"] >= length
					intl_rates_df_max_w_filter = temp_df["Max W (cm)"] >= width
					intl_rates_df_max_h_filter = temp_df["Max H (cm)"] >= height
					intl_rates_df_max_lenwidhei_filter = temp_df["Max L+W+H (cm)"] >= lenwidhei
					intl_rates_df_max_lengir_filter = temp_df["Max L+2W+2H (cm)"] >= lengir

					temp_df = temp_df[(intl_rates_df_max_l_filter) &
									  (intl_rates_df_max_w_filter) &
									  (intl_rates_df_max_h_filter) &
									  (intl_rates_df_max_lenwidhei_filter) &
									  (intl_rates_df_max_lengir_filter)
									 ]

				for i, row in temp_df.iterrows():
					transit_times_filter = times_df["Service"].apply(lambda s: True if s in row["SingPost Service"] else False)
					earliest_transit = times_df[transit_times_filter].iloc[0]["Earliest Time (days)"]
					if earliest_transit != 0.08:
						earliest_transit = int(earliest_transit)
					latest_transit = times_df[transit_times_filter].iloc[0]["Latest Time (days)"]
					insurance = times_df[transit_times_filter].iloc[0]["Insurance"]
					home_pick_up = times_df[transit_times_filter].iloc[0]["Home Pick Up"]

					singpost_estimates.append({"Service Provider" : "SingPost",
											   "Service" : row["SingPost Service"],
											   "Estimated Rate" : round(row["Rate in SGD"], 2),
											   "Estimated Transit Time" : (earliest_transit, latest_transit),
											   "Other Remarks" : row["Remarks"],
											   "Insurance" : insurance,
											   "Re Delivery" : 2,
											   "Home Pick Up" : home_pick_up
											  }
											 )
		
	return singpost_estimates

def get_shipping_estimates(dest_country, weight, weight_unit="kg", dim_lwh=(None, None, None), dim_unit="cm"):
	
	shipping_estimates = []
	
	if weight_unit == "lbs":
		weight *= 0.453592
		weight_unit = "kg"
	
	dim_given = False
	if ((dim_lwh[0] != None) and (dim_lwh[1] != None) and (dim_lwh[2] != None)):
		dim_given = True
	
	if dim_given:
		if dim_unit == "in":
			dim_lwh[0] *= 2.54
			dim_lwh[1] *= 2.54
			dim_lwh[2] *= 2.54
			dim_unit = "cm"
	
	current_relpath = os.path.relpath(inspect.getfile(get_shipping_estimates))
	data_assets_relpath = os.path.join(os.path.split(current_relpath)[0], "data_assets")

	try:
		countries_data_relpath = os.path.join(data_assets_relpath, "Countries List.csv")
		countries_df = pd.read_csv(countries_data_relpath)
		dest_country = countries_df[countries_df["Country Code"] == dest_country]["Country Name"].iloc[0]
	except:
		print("ERROR READING DATA EXCEL FILES!")

	fedex_estimates = get_fedex_estimates(data_assets_relpath, dest_country, weight, dim_given, dim_lwh)
	shipping_estimates.extend(fedex_estimates)

	dhl_estimates = get_dhl_estimates(data_assets_relpath, dest_country, weight, dim_given, dim_lwh)
	shipping_estimates.extend(dhl_estimates)

	singpost_estimates = get_singpost_estimates(data_assets_relpath, dest_country, weight, dim_given, dim_lwh)
	shipping_estimates.extend(singpost_estimates)

	ups_estimates = get_ups_estimates(data_assets_relpath, dest_country, weight, dim_given, dim_lwh)
	shipping_estimates.extend(ups_estimates)
	
	return shipping_estimates