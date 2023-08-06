use pyo3::prelude::*;
use rust_decimal::Decimal;

pub const SCALE_MASK: u32 = 0x00FF_0000;
pub const SIGN_MASK: u32 = 0x8000_0000;
pub const SCALE_SHIFT: u32 = 16;

pub fn is_sign_negative(flags: &u32) -> bool {
    flags & SIGN_MASK > 0
}

pub fn scale(flags: &u32) -> u32 {
    ((flags & SCALE_MASK) >> SCALE_SHIFT) as u32
}
/// Returns string representation of decimal created from parts
#[pyfunction]
fn rust_decimal_raw_parts_to_string(lo: u32, mid: u32, hi: u32, flags: u32) -> PyResult<String> {
    let negative = is_sign_negative(&flags);
    let scale = scale(&flags);
    let decimal = Decimal::from_parts(lo, mid, hi, negative, scale);
    Ok(decimal.to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn vybe_solana_helpers(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(rust_decimal_raw_parts_to_string, m)?)?;
    Ok(())
}
