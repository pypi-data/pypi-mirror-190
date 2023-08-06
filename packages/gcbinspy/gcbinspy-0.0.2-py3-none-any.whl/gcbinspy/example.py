import gcbinspy

address = "26 Eleventh Ave, Palm Beach QLD 4221"
pid = "0602988f-8716-4743-81e3-781f4fd341c7"

client = gcbinspy.GoldCoastBins(address)
client.property_id()
client.update_next_bin_days()
print(client.next_landfill().isoformat())
print(client.is_recycling_day())
print(client.is_organics_day_tomorrow())