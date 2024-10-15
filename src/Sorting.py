from MinHeap import MinHeap
from Vehicle import Vehicle

vehicles = [Vehicle("123"), Vehicle("456"), Vehicle("789")]
vehicles[0].set_distance_to_destination(10)
vehicles[1].set_distance_to_destination(5)
vehicles[2].set_distance_to_destination(20)

h = MinHeap(len(vehicles))
sorted_vehicles = h.heapsort_vehicles(vehicles)
for i in sorted_vehicles:
    print(i.get_distance_to_destination())