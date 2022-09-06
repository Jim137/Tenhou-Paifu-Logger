// This file is a derived version of Mortal:/libriichi/src/tile.rs

use crate::{matches_tu8, t, tu8};
use std::cmp::Ordering;
use std::error::Error;
use std::fmt;
use std::str::FromStr;

use boomphf::hashmap::BoomHashMap;
use once_cell::sync::Lazy;
use serde::{Deserialize, Deserializer, Serialize, Serializer};

const MJAI_PAI_STRINGS_LEN: usize = 3 * 9 + 4 + 3 + 3 + 1;
const MJAI_PAI_STRINGS: [&str; MJAI_PAI_STRINGS_LEN] = [
    "1m", "2m", "3m", "4m", "5m", "6m", "7m", "8m", "9m", // m
    "1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p", // p
    "1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", // s
    "E", "S", "W", "N", "P", "F", "C", // z
    "5mr", "5pr", "5sr", // a
    "?",   // unknown
];

static MJAI_PAI_STRINGS_MAP: Lazy<BoomHashMap<&'static str, Tile>> = Lazy::new(|| {
    let mut values = vec![];
    for id in 0..MJAI_PAI_STRINGS_LEN {
        values.push(Tile::try_from(id).unwrap());
    }
    BoomHashMap::new(MJAI_PAI_STRINGS.to_vec(), values)
});

#[derive(Default, Clone, Copy, PartialEq, Eq, Hash)]
pub struct Tile(u8);

impl Tile {
    const MAX: usize = MJAI_PAI_STRINGS_LEN - 1;

    /// # Safety
    /// Calling this method with an out-of-bounds tile ID is undefined behavior.
    #[inline]
    #[must_use]
    pub const unsafe fn new_unchecked(id: u8) -> Self {
        Self(id)
    }

    #[inline]
    #[must_use]
    pub const fn as_u8(self) -> u8 {
        self.0
    }
    #[inline]
    #[must_use]
    pub const fn as_usize(self) -> usize {
        self.0 as usize
    }

    #[inline]
    #[must_use]
    pub const fn deaka(self) -> Self {
        match self.0 {
            tu8!(5mr) => t!(5m),
            tu8!(5pr) => t!(5p),
            tu8!(5sr) => t!(5s),
            _ => self,
        }
    }

    #[inline]
    #[must_use]
    pub const fn akaize(self) -> Self {
        match self.0 {
            tu8!(5m) => t!(5mr),
            tu8!(5p) => t!(5pr),
            tu8!(5s) => t!(5sr),
            _ => self,
        }
    }

    #[inline]
    #[must_use]
    pub const fn is_aka(self) -> bool {
        matches_tu8!(self.0, 5mr | 5pr | 5sr)
    }

    #[inline]
    #[must_use]
    pub const fn is_jihai(self) -> bool {
        matches_tu8!(self.0, E | S | W | N | P | F | C)
    }

    #[inline]
    #[must_use]
    pub const fn is_yaokyuu(self) -> bool {
        matches_tu8!(
            self.0,
            1m | 9m | 1p | 9p | 1s | 9s | E | S | W | N | P | F | C
        )
    }

    #[inline]
    #[must_use]
    pub const fn next(self) -> Self {
        let tile = self.deaka();
        let kind = tile.0 / 9;
        let num = tile.0 % 9;

        if kind < 3 {
            Self(kind * 9 + (num + 1) % 9)
        } else if num < 4 {
            Self(3 * 9 + (num + 1) % 4)
        } else {
            Self(3 * 9 + 4 + (num - 4 + 1) % 3)
        }
    }

    #[inline]
    #[must_use]
    pub const fn prev(self) -> Self {
        let tile = self.deaka();
        let kind = tile.0 / 9;
        let num = tile.0 % 9;
        if kind < 3 {
            Self(kind * 9 + (num + 9 - 1) % 9)
        } else if num < 4 {
            Self(3 * 9 + (num + 4 - 1) % 4)
        } else {
            Self(3 * 9 + 4 + (num - 4 + 3 - 1) % 3)
        }
    }

    const fn as_ord(self) -> impl Ord {
        let id = self.0;
        match id {
            tu8!(5mr) => 4,
            tu8!(5pr) => 14,
            tu8!(5sr) => 24,
            _ => {
                let kind = id / 9;
                let num = id % 9;
                let ord_id = kind * 10 + num;
                match ord_id {
                    4..=8 | 14..=18 | 24..=28 => ord_id + 1,
                    _ => ord_id,
                }
            }
        }
    }
}

#[derive(Debug)]
pub enum InvalidTile {
    Number(usize),
    String(String),
}

impl TryFrom<u8> for Tile {
    type Error = InvalidTile;

    fn try_from(v: u8) -> Result<Self, Self::Error> {
        Self::try_from(v as usize)
    }
}

impl TryFrom<usize> for Tile {
    type Error = InvalidTile;

    fn try_from(v: usize) -> Result<Self, Self::Error> {
        if v > Tile::MAX {
            Err(InvalidTile::Number(v))
        } else {
            // SAFETY: `v` has been proven to be in bound.
            let tile = unsafe { Self::new_unchecked(v as u8) };
            Ok(tile)
        }
    }
}

impl FromStr for Tile {
    type Err = InvalidTile;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        MJAI_PAI_STRINGS_MAP
            .get(s)
            .copied()
            .ok_or_else(|| InvalidTile::String(s.to_owned()))
    }
}

impl fmt::Debug for Tile {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        fmt::Display::fmt(&self, f)
    }
}

impl fmt::Display for Tile {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        // SAFETY: `Tile` is in-bound iff it is constructed safely.
        let s = unsafe { MJAI_PAI_STRINGS.get_unchecked(self.0 as usize) };
        f.write_str(s)
    }
}

impl<'de> Deserialize<'de> for Tile {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        let tile = String::deserialize(deserializer)?
            .parse()
            .map_err(serde::de::Error::custom)?;
        Ok(tile)
    }
}

impl Serialize for Tile {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        serializer.collect_str(self)
    }
}

impl Ord for Tile {
    fn cmp(&self, other: &Self) -> Ordering {
        self.as_ord().cmp(&other.as_ord())
    }
}

impl PartialOrd for Tile {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl fmt::Display for InvalidTile {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str("not a valid tile: ")?;
        match self {
            Self::Number(n) => fmt::Display::fmt(n, f),
            Self::String(s) => write!(f, "not a valid tile: \"{s}\""),
        }
    }
}

impl Error for InvalidTile {}

#[must_use]
pub fn tile_set_eq(a: &[Tile], b: &[Tile], ignore_aka: bool) -> bool {
    if a.len() != b.len() {
        return false;
    }

    let mut a_bits = 0u64;
    let mut b_bits = 0u64;
    for &t in a {
        let id = if ignore_aka { t.deaka() } else { t }.as_u8();
        a_bits |= 0b1 << id;
    }
    for &t in b {
        let id = if ignore_aka { t.deaka() } else { t }.as_u8();
        b_bits |= 0b1 << id;
    }

    a_bits == b_bits
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn next_prev() {
        MJAI_PAI_STRINGS.iter().take(37).for_each(|&s| {
            let tile: Tile = s.parse().unwrap();
            assert_eq!(tile.prev().next(), tile.deaka());
            assert_eq!(tile.next().prev(), tile.deaka());
        });
    }
}
