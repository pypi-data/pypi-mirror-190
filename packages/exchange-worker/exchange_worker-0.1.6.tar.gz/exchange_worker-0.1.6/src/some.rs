use std::sync::atomic::AtomicBool;

use binance::api::*;
use binance::config::Config;
use binance::websockets::*;
use binance::ws_model::{CombinedStreamEvent, WebsocketEvent, WebsocketEventUntag};

use futures::future::BoxFuture;
use futures::stream::StreamExt;
use tokio::sync::mpsc::UnboundedSender;
use tokio_tungstenite::tungstenite::Message;
use crate::binance_connector::{BinanceListener, BinanceListenerOptions};

mod binance_connector;
mod python;

#[tokio::main]
async fn main() {
    let tickers = vec![book_ticker_stream("btcusdt")];
    let it: BinanceListener = BinanceListener::new(Some("ff".to_string()));
    let opts = BinanceListenerOptions::new(tickers);
    let handler = move |t: WebsocketEventUntag| {
        // let guard = Python::acquire_gil();
        // let py = guard.python();

        match t {
            WebsocketEventUntag::BookTicker(event) => {
                let tick = python::models::TickData {
                    update_id: event.update_id,
                    symbol: event.symbol,
                    bid: event.best_bid.to_string(),
                    bid_size: event.best_bid_qty.to_string(),
                    ask: event.best_ask.to_string(),
                    ask_size: event.best_ask_qty.to_string(),
                };

                dbg!(&tick);
                // callback.call(py, (tick, ), None).expect("TODO: panic message");
            }
            _ => {}
        };
    };
    it.subscribe(opts, &handler);
}

async fn some() {
    let (logger_tx, mut logger_rx) = tokio::sync::mpsc::unbounded_channel::<WebsocketEvent>();
    // let (close_tx, mut close_rx) = tokio::sync::mpsc::unbounded_channel::<bool>();
    // let wait_loop = tokio::spawn(async move {
    //     'hello: loop {
    //         tokio::select! {
    //             event = logger_rx.recv() => println!("{event:?}"),
    //             _ = close_rx.recv() => break 'hello
    //         }
    //     }
    // });

    let streams: Vec<BoxFuture<'static, ()>> = vec![
        Box::pin(connect(logger_tx.clone())),
        // Box::pin(combined_orderbook(logger_tx.clone())),
    ];

    for stream in streams {
        tokio::spawn(stream);
    }

    tokio::select! {
        // _ = wait_loop => { println!("Finished!") }
        _ = tokio::signal::ctrl_c() => {
            println!("Closing websocket stream...");
            // close_tx.send(true).unwrap();
            tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;
        }
    }
}

#[allow(dead_code)]
async fn connect(logger_tx: UnboundedSender<WebsocketEvent>) {
    let keep_running = AtomicBool::new(true);
    let book_ticker: String = book_ticker_stream("btcusdt");
    let streams: Vec<String> = vec!["btcusdt", "ethusdt"]
        .into_iter()
        .map(|symbol| partial_book_depth_stream(symbol, 5, 1000))
        .collect();

    let config = Config { ws_endpoint: "wss://fstream.binance.com".into(), ..Config::default() };
    let mut web_socket: WebSockets<'_, CombinedStreamEvent<_>> =
        WebSockets::new_with_options(|event: CombinedStreamEvent<WebsocketEventUntag>| {
            if let WebsocketEventUntag::WebsocketEvent(we) = &event.data {
                // logger_tx.send(we.clone()).unwrap();
            }
            let data = event.data;
            if let WebsocketEventUntag::BookTicker(orderbook) = data {
                println!("{orderbook:?}")
            }
            Ok(())
        }, config);

    let endpoints = vec![book_ticker];
    web_socket.connect_multiple(endpoints).await.unwrap(); // check error

    // web_socket.connect(&book_ticker).await.unwrap(); // check error
    if let Err(e) = web_socket.event_loop(&keep_running).await {
        println!("Error: {e}");
    }
    web_socket.disconnect().await.unwrap();
    println!("disconnected");
}