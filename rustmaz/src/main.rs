use serde::Serialize;
use std::{fmt, fs};
use std::collections::HashSet;
use rand::{Rng, thread_rng};

#[derive(Eq, Hash, PartialEq, Copy, Clone, Serialize)]
enum Wall {
    Top = 0,
    Bottom = 1,
    Left = 2,
    Right = 3,
}

impl Wall {
    fn from_u8(value: u8) -> Wall {
        match value {
            0 => Wall::Top,
            1 => Wall::Bottom,
            2 => Wall::Left,
            3 => Wall::Right,
            _ => panic!("TOO BIG BRO!")
        }
    }
}

#[derive(Clone, PartialEq)]
struct Cell {
    walls: HashSet<Wall>,
    coords: (usize, usize),
}

impl Cell {
    fn new(coords: (usize, usize)) -> Self {
        let walls = [Wall::Top, Wall::Bottom, Wall::Left, Wall::Right];
        Cell { walls: HashSet::from(walls), coords }
    }
    fn from(walls: u8) -> Self {
        let mut wallset = HashSet::new();
        if walls >> 0 & 1 == 1 {
            wallset.insert(Wall::Top);
        }
        if walls >> 1 & 1 == 1 {
            wallset.insert(Wall::Bottom);
        }
        if walls >> 2 & 1 == 1 {
            wallset.insert(Wall::Left);
        }
        if walls >> 3 & 1 == 1 {
            wallset.insert(Wall::Right);
        }
        Cell { walls: wallset, coords: (0, 0) }
    }
    fn to_u8(&self) -> u8 {
        let mut output: u8 = 0x00;
        for wall in &self.walls {
            output |= (self.walls.contains(&wall) as u8) << (*wall as u8);
        }
        output
    }
    fn set_wall(&mut self, value: bool, side: Wall) {
        if value {
            self.walls.insert(side);
        } else {
            self.walls.remove(&side);
        }
    }
}

struct Maz {
    value: Vec<u8>,
    size: usize,
    in_maze_list: Vec<(usize, usize)>,
    cells: Vec<Cell>,
    to_add: Vec<(usize, usize)>,
    to_add_ref: Vec<(usize, usize)>

}

impl fmt::Debug for Maz {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        fmt::Debug::fmt(&**self, f)
    }
}

impl std::ops::Deref for Maz {
    type Target = Vec<u8>;

    fn deref(&self) -> &Self::Target {
        &self.value
    }
}

impl Maz {
    fn new(size: usize) -> Self {
        let mut i: usize = 0;
        let total_size: usize = size * size;
        let mut val_holder: Vec<u8> = vec![];
        let mut cell_holder: Vec<Cell> = vec![];
        let mut curr_x: usize = 0;
        let mut curr_y: usize = 0;
        while i < total_size {
            val_holder.push(0);
            cell_holder.push(Cell::new((curr_x, curr_y)));
            if curr_x < size - 1 {
                curr_x = curr_x + 1;
            } else {
                curr_y = curr_y + 1;
                curr_x = 0;
            }
            i = i + 1;
        }
        Maz { value: val_holder, size, in_maze_list: vec![], cells: cell_holder, to_add: vec![], to_add_ref: vec![]}
    }
    fn generate(&mut self) {
        let mut coords= (0, 0);
        let mut prevlist: Vec<(usize, usize)> = vec![];
        let mut tried = (false, false, false, false);
        loop {
            tried = (false, false, false, false);
            if self.to_add.contains(&coords) {
                let mut curr_index = self.get_index_of_cell_ta(coords.0, coords.1)
                self.to_add.remove(curr_index);
                self.to_add_ref.remove(curr_index);
            }
            if coords.1 > 0 &&
                !self.in_maze_list.contains(&(coords.0, coords.1 - 1)) &&
                !self.to_add.contains(&(coords.0, coords.1 - 1)){
                self.to_add.push((coords.0, coords.1 - 1));
                self.to_add_ref.push(coords);
            } else {
                tried.0 = true;
            }
            if coords.1 + 1 < self.size &&
                !self.in_maze_list.contains(&(coords.0, coords.1 + 1)) &&
                !self.to_add.contains(&(coords.0, coords.1 + 1)) {
                self.to_add.push((coords.0, coords.1 + 1));
                self.to_add_ref.push(coords);
            } else {
                tried.1 = true;
            }
            if coords.0 > 0 &&
                !self.in_maze_list.contains(&(coords.0 - 1, coords.1)) &&
                !self.to_add.contains(&(coords.0 - 1, coords.1)) {
                self.to_add.push((coords.0 - 1, coords.1));
                self.to_add_ref.push(coords);
            } else {
                tried.2 = true;
            }
            if coords.0 + 1 < self.size &&
                !self.in_maze_list.contains(&(coords.0 + 1, coords.1)) &&
                !self.to_add.contains(&(coords.0 + 1, coords.1)) {
                self.to_add.push((coords.0 + 1, coords.1));
                self.to_add_ref.push(coords);
            } else {
                tried.3 = true;
            }
            let mut ran = rand::thread_rng().gen_range(0..self.to_add.len());
            coords = self.to_add[ran];
                if tried.0 && tried.1 && tried.2 && tried.3 {
                    if prevlist.len() == 0 {
                        return;
                    }
                } else {
                    break;
                }
            }
        let mut next_side = random_side();
        let mut next_coords = coords;
        loop {
            match next_side {
                Wall::Top => {
                    if self.to_add.contains() {
                        next_coords = (coords.0, coords.1 - 1);
                        break;
                    } else {
                        next_side = random_side();
                    }
                }
                Wall::Bottom => {
                    if !tried.1 {
                        next_coords = (coords.0, coords.1 + 1);
                        break;
                    } else {
                        next_side = random_side();
                    }
                }
                Wall::Left => {
                    if !tried.2 {
                        next_coords = (coords.0 - 1, coords.1);
                        break;
                    } else {
                        next_side = random_side();
                    }
                }
                Wall::Right => {
                    if !tried.3 {
                        next_coords = (coords.0 + 1, coords.1);
                        break;
                    } else {
                        next_side = random_side();
                    }
                }
            };

            self.coords = self.to_add_ref[self.get_index_of_cell_ta(next_coords.0, next_coords.1)];

            if !self.in_maze_list.contains(&next_coords) {
                self.in_maze_list.push(coords);
                self.open_border(coords, next_coords);
                prevlist.push(coords);
                coords = next_coords;
            } else {
                self.in_maze_list.push(next_coords);
                self.open_border(coords, next_coords);
            }
            if self.to_add.len() <= 0 && self.in_maze_list.len() == (self.size * self.size) as usize {
                break;
            }
        }
    }
    fn get_value_at(&self, x: usize, y: usize) -> u8 {
        self.value[((&self.size * x) + y) as usize]
    }
    fn set_value_at(&mut self, x: usize, y: usize, value: u8) {
        self.value[((&self.size * x) + y) as usize] = value;
    }
    fn get_index_of_cell_im(&self, x: usize, y: usize) -> usize {
        for cell in 0..self.cells.len() {
            if self.cells[cell].coords == (x, y) {
                return cell
            }
        }
        0
    }
    fn get_index_of_cell_ta(&self, x: usize, y: usize) -> usize {
        for cell in 0..self.to_add.len() {
            if self.to_add[cell] == (x, y) {
                return cell
            }
        }
        0
    }
    fn open_border(&mut self, a: (usize, usize), b: (usize, usize)) {
        let y1 = a.0 as isize;
        let y2 = b.0 as isize;
        let x1 = a.1 as isize;
        let x2 = b.1 as isize;

        let val1 = self.get_index_of_cell_im(a.0, a.1) as usize;
        let sides1 = self.cells[self.get_index_of_cell_im(a.0, a.1)].to_u8();
        let val2 = self.get_index_of_cell_im(b.0, b.1) as usize;
        let sides2 = self.cells[self.get_index_of_cell_im(b.0, b.1)].to_u8();

        if x2 - x1 == 1 {
            self.value[val1] = to_encoded(false, sides1, Wall::Left);
            self.value[val2] = to_encoded(false, sides2, Wall::Right);
        } else if x1  - x2  == 1 {
            self.value[val1] = to_encoded(false, sides1, Wall::Right);
            self.value[val2] = to_encoded(false, sides2, Wall::Left);
        } else if y2  - y1  == 1 {
            self.value[val1] = to_encoded(false, sides1, Wall::Top);
            self.value[val2] = to_encoded(false, sides2, Wall::Bottom);
        } else if y1  - y2  == 1 {
            self.value[val1] = to_encoded(false, sides1, Wall::Bottom);
            self.value[val2] = to_encoded(false, sides2, Wall::Top);
        }
    }
}

fn random_side() -> Wall {
    Wall::from_u8(thread_rng().gen_range((Wall::Top as u8)..(Wall::Right as u8) + 1))
}

fn to_encoded(value: bool, initial: u8, side: Wall) -> u8 {
    let mut temp = Cell::from(initial);
    temp.set_wall(value, side);
    temp.to_u8()
}

fn main() {
    //let size: usize = rand::thread_rng().gen_range(2..41);
    let size= 30;
    let mut bob = Maz::new(size);
    bob.generate();

    //bob.value = vec![0b1010, 0b1000, 0b1001, 0b0010, 0b0000, 0b0001, 0b0110, 0b0100, 0b0101];

    //let mut rand = thread_rng();

    /* for x in 0..bob.get_size() {
        for y in 0..bob.get_size() {
            bob.set_at(x, y, rand.gen_range(0..16));
        }
    } */

    println!("{:?}", bob);
    println!("{:#04b}", bob.cells[0].to_u8());
    let bobser = serde_pickle::to_vec(&bob.value, Default::default()).unwrap();

    fs::write("./currmaze.mazdat", &bobser).unwrap();
}
