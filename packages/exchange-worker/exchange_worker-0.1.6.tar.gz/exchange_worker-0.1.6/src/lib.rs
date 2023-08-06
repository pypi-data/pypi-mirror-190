use std::sync::Arc;

use pyo3::prelude::*;
use futures::{pin_mut, StreamExt};
use futures::future::select;
use pyo3::types::{IntoPyDict, PyDict};
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio_tungstenite::{connect_async, tungstenite::protocol::Message};

use crate::binance_connector::BinanceTick;
use crate::python::models::TickData;

#[allow(unused_variables)]
mod binance_connector;
mod python;

#[pyfunction]
fn some(py: Python) -> PyResult<&PyAny> {
    let tick = PyModule::import(py, "nautilus_trader.model.data.tick").unwrap();
    let qt = tick.getattr("QuoteTick").unwrap();

    let key_vals: Vec<(&str, PyObject)> = vec![
        ("instrument_id", "BTCUSD-PERP.BINANCE".to_object(py)),
        ("bid", "11".to_object(py)),
        ("ask", "22".to_object(py)),
        ("bid_size", "111".to_object(py)),
        ("ask_size", "222".to_object(py)),
        ("update_id", "3333333".to_object(py)),
        ("ts_event", 4444444.to_object(py)),
        ("ts_init", 5555555.to_object(py)),
    ];
    let dict = key_vals.into_py_dict(py);
    let qt_instance = qt.call_method1("from_dict", (dict, )).expect("QT error");
    Ok(qt_instance)
}

#[pyfunction]
fn rust_sleep(py: Python) -> PyResult<&PyAny> {
    pyo3_asyncio::tokio::future_into_py(py, async {
        tokio::time::sleep(std::time::Duration::from_secs(1)).await;
        Ok(())
    })
}

#[pyclass]
struct ExchangeListener {
    // token: Option<String>,
}

#[pymethods]
impl ExchangeListener {
    #[new]
    fn new() -> ExchangeListener {
        ExchangeListener {}
    }

    fn subscribe<'a>(&'a self, py: Python<'a>, tickers: Vec<String>, callback: PyObject) -> PyResult<&PyAny> {
        pyo3_asyncio::tokio::future_into_py(py, async move {
            let streams = tickers.iter().map(|t| format!("{t}@bookTicker")).collect::<Vec<String>>().join("/");
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
                    let _ = Python::with_gil(|py| {
                        let data = message.unwrap().into_data();
                        let tick: BinanceTick = serde_json::from_slice(&data).unwrap();
                        // let tick_data: TickData = tick.into();
                        let instrument_id = format!("{}-PERP.BINANCE", tick.data.s);

                        // Form Tick
                        let tick_module = PyModule::import(py, "nautilus_trader.model.data.tick").unwrap();
                        let qt_class = tick_module.getattr("QuoteTick").unwrap();

                        let key_vals: Vec<(&str, PyObject)> = vec![
                            ("instrument_id", instrument_id.to_object(py)),
                            ("bid", tick.data.b.to_object(py)),
                            ("ask", tick.data.a.to_object(py)),
                            ("bid_size", tick.data.B.to_object(py)),
                            ("ask_size", tick.data.A.to_object(py)),
                            ("update_id", tick.data.u.to_object(py)),
                            ("ts_event", tick.data.E.to_object(py)),
                            ("ts_init", tick.data.T.to_object(py)),
                        ];
                        let dict = key_vals.into_py_dict(py);
                        let qt_instance = qt_class.call_method1("from_dict", (dict, )).expect("QT error");

                        cb.clone().call(py, (qt_instance, ), None).expect("wrong");
                    });
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
}


/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn exchange_worker(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<ExchangeListener>()?;
    m.add_class::<TickData>()?;
    m.add_function(wrap_pyfunction!(rust_sleep, m)?)?;
    m.add_function(wrap_pyfunction!(some, m)?)?;
    Ok(())
}