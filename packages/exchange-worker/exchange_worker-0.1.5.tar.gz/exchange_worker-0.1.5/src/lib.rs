use std::collections::HashMap;
use std::sync::Arc;

use futures::{pin_mut, StreamExt};
use futures::future::select;
use pyo3::prelude::*;
use serde_json::Value;
// use futures_util::{future};
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio_tungstenite::{connect_async, tungstenite::protocol::Message};

use crate::binance_connector::{BinanceListener, BinanceListenerOptions, BinanceTick};
use crate::python::models::TickData;

#[allow(unused_variables)]
mod binance_connector;
mod python;

#[pyclass]
struct ExchangeListener {
    // token: Option<String>,
}

#[pyfunction]
fn rust_sleep(py: Python) -> PyResult<&PyAny> {
    pyo3_asyncio::tokio::future_into_py(py, async {
        tokio::time::sleep(std::time::Duration::from_secs(1)).await;
        Ok(())
    })
}

#[pymethods]
impl ExchangeListener {
    #[new]
    fn new() -> ExchangeListener {
        ExchangeListener {}
    }

    fn subscribe<'a>(&'a self, py: Python<'a>, tickers: Vec<String>, callback: PyObject) -> PyResult<&PyAny> {
        pyo3_asyncio::tokio::future_into_py(py, async move {
            // let it: BinanceListener = BinanceListener::new();
            // let opts = BinanceListenerOptions::new(tickers);
            let streams = tickers.iter().map(|t|format!("{t}@bookTicker")).collect::<Vec<String>>().join("/");
            let url = url::Url::parse(format!("wss://fstream.binance.com/stream?streams={streams}").as_str()).unwrap();
            let (stdin_tx, stdin_rx) = futures_channel::mpsc::unbounded();

            tokio::spawn(read_stdin(stdin_tx));

            let (ws_stream, _) = connect_async(url).await.expect("Failed to connect");
            println!("WebSocket handshake has been successfully completed");

            let (write, read) = ws_stream.split();
            let cb = Arc::new(callback);

            let stdin_to_ws = stdin_rx.map(Ok).forward(write);
            let ws_to_stdout = {
                read.for_each(|message| async {
                    let guard = Python::acquire_gil();
                    let py = guard.python();
                    let data = message.unwrap().into_data();
                    let tick: BinanceTick = serde_json::from_slice(&data).unwrap();
                    let tick_data: TickData = tick.into();
                    // dbg!(&tick_data);

                    &cb.clone().call(py, (tick_data, ), None).expect("wrong");
                })
            };

            pin_mut!(stdin_to_ws, ws_to_stdout);
            select(stdin_to_ws, ws_to_stdout).await;

            async fn read_stdin(tx: futures_channel::mpsc::UnboundedSender<Message>) {
                let mut stdin = tokio::io::stdin();
                loop {
                    let mut buf = vec![0; 1024];
                    let n = match stdin.read(&mut buf).await {
                        Err(_) | Ok(0) => break,
                        Ok(n) => n,
                    };
                    buf.truncate(n);
                    tx.unbounded_send(Message::binary(buf)).unwrap();
                }
            }
            Ok(())
        })
    }


    fn sleep<'a>(&'a self, py: Python<'a>) -> PyResult<&PyAny> {
        pyo3_asyncio::tokio::future_into_py(py, async {
            tokio::time::sleep(std::time::Duration::from_secs(1)).await;
            Ok(())
        })
    }
}


/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn exchange_worker(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<ExchangeListener>()?;
    m.add_class::<TickData>()?;
    m.add_function(wrap_pyfunction!(rust_sleep, m)?)?;
    Ok(())
}