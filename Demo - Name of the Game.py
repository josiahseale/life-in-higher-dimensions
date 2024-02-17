import itertools
import pandas as pd

# The first integer here below (218051617... etc.) is the integer for OG Conway's Game of Life.
#name_of_the_game = 2180516173394519435132181751419793678696100887287477573983491194161129871770326488003228200834079588279326074400248049602259123681421440
#name_of_the_game = 12281893100684602514411016534685167309701510867261703451386396385233280767300903976713074062184159923723658981003852061609271277849956089989464956749578518
#name_of_the_game = 6243592368837255341964943694885221325910330536568224422601534950590759745111520330923516825416225322917739525205768639805370377878704534568567062
#name_of_the_game = 204586912993510323614300289574887305519985430096840508859510186813864539965037884121732429731567878230991845313246676181806397758081205177813991172374
#name_of_the_game = 78804012392788958424558080201281874082979051825241657832190228488692355889190607054770706746627605268242069406613780
#name_of_the_game = 20
#name_of_the_game = 511
#name_of_the_game = 387381625547900589334 #this integer and the following together show convergence in emergence. They are very different numbers and produce patterns that differ yet have similar characteristics.
#name_of_the_game = 169232910299583734436674453987840461901162486938031519657372081911173685352747857183990045137982186801626620740500793585631232
#name_of_the_game = 22181357552966518876627313473144669627491496603014121267516182636416445034089519365198276641489333995549206915554012804501001535490
#name_of_the_game = 29073549059825450931264526289022309518443549051813237739040592699270412313403403338697486445702047122551937325082678161185392502849536278
#name_of_the_game = 11090678776483259438313656736572334813745748301503266416474007559774680654793487500847805478026825344951067346766572902665089515522
#name_of_the_game = 22181357552966558278633509867623884042518633164853658338584883232357127943676633561543716208694925373492673683420834092634868023572
name_of_the_game = 8829487448431316450667164497543080343250462146801803111914052745429809669826753258024542038296352014535712394143840787693495094993011851965965972173438780


number_of_iterations = 63
number_of_dimensions = 2
origin = tuple([0] * number_of_dimensions)
cols = ["X", "Y"]  # label the dimensions whatever you want, just for the output data set
starting_board = {origin}
#starting_board = {(0, 0), (0, -1), (0, 1), (-1, 0), (1, 1)}    # R-Pentomino Configuration -- Mainly for use with the OG Conway integer. to see that it's actually Conway's Game of Life

class Board:
    def __init__(self, alive):
        self.alive = set(alive)
        self.universe = self.get_universe()
        self.magic_sort = sorted(list(self.get_neighborhood(origin)), key=self.custom_sort, reverse=True) # Fun math wrinkle: the so-called "magic sort" is only ever used once, as a perspective on the origin and the n-dimensional infinitesimals surrounding it, and all subsequent n-dimensional configurations are represented as partial realizations based on this.

    @staticmethod
    def get_neighborhood(coord):
        """Get the surrounding coordinates for a given coordinate"""
        return set(itertools.product(*[(axis - 1, axis, axis + 1) for axis in coord]))

    @staticmethod
    def custom_sort(coord):
        # This ordering prioritizes the 0s, then 1s, then -1s. Try flipping the "1" to "-1" to observe the property that the "magic sort" order doesn't much matter.
        def priority(val):
            if val == 0:
                return 0
            elif val == 1:
                return 1
            else:
                return 2
        return tuple(priority(val) for val in coord)

    def get_universe(self):
        """Include all alive cells and their neighbors."""
        universe = self.alive.copy()
        for coord in self.alive:
            universe.update(self.get_neighborhood(coord))
        return universe

    def offset_neighbor_by_coordinate(self, coordinate, neighbor):      #this method just expresses a coordinate's neighbor's value in reference to the coordinate: if you are (100, 100) and I am (99, 99), then as far as you are concerned, I am a (-1, -1).
        offset_neighbor = tuple(neighbor_axis - reference_axis for neighbor_axis, reference_axis in zip(neighbor, coordinate))
        return offset_neighbor

    def get_index(self, coord):
        coordinate_neighborhood = self.get_neighborhood(coord)
        coordinate_live_neighbors = coordinate_neighborhood.intersection(self.alive)
        offset_live_neighbors = tuple(self.offset_neighbor_by_coordinate(coord, neighbor) for neighbor in coordinate_live_neighbors)

        # Create the index for the coord.
        index = 0
        for neighbor in self.magic_sort:
            if neighbor in offset_live_neighbors:
                index = (index << 1) | 1
            else:
                index <<= 1
        return index

    def check_alive(self, coord):
        index = self.get_index(coord)
        return name_of_the_game >> index & 1

    def next(self):
        new_universe = {coord for coord in self.universe if self.check_alive(coord)}
        return Board(new_universe)

if __name__ == "__main__":
    board = Board(starting_board)
    output_data = [[0] + list(coord) for coord in starting_board]
    output_dataset = pd.DataFrame(output_data, columns=['Iter'] + cols)
    for i in range(number_of_iterations):
        board = board.next()
        new_data = [[i + 1] + list(coord) for coord in board.alive]
        output_dataset = pd.concat([output_dataset, pd.DataFrame(new_data, columns=['Iter'] + cols)])
    print(f"Universe Size at Last Iteration: {len(board.universe)} \tLiving Cells at Last Iteration: {len(board.alive)}")
    output_dataset.to_csv(f'C:\\Users\\User\\Downloads\\Output - Data.csv', index=False)
