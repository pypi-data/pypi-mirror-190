use pyo3::prelude::*;
//use std::ffi::{CStr, c_char}; 
use openai_api_client::*;

#[actix_rt::main]
#[pyfunction] 
async fn get_answer(python_string: &str, my_max_tokens: u32, my_api_key: &str) -> PyResult<String> {
    //let bytes = unsafe { CStr::from_ptr(python_string).to_bytes() };
    //let rust_string: &str = std::str::from_utf8(bytes).unwrap();
        
    let api_key = my_api_key;
    let model = "text-davinci-003";
    let max_tokens:u32 = my_max_tokens;
    let prompt = python_string.trim();

    let answer: String = completions_pretty(prompt, model, max_tokens, &api_key).await;

    Ok(answer)
}

/// A Python module implemented in Rust.
#[pymodule]
fn openai_simple(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_answer, m)?)?;
    Ok(())
}