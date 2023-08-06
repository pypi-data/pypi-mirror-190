use std::sync::atomic::AtomicBool;

use serde::Deserialize;
use binance::config::Config;
use binance::websockets::*;
use binance::ws_model::{BookTickerEvent, CombinedStreamEvent, WebsocketEvent, WebsocketEventUntag};
// use futures::stream::StreamExt;
use tokio::select;

type Callback<'a> = dyn Fn(Box<BookTickerEvent>) -> () + Send + 'static;

#[allow(non_snake_case)]
#[derive(Debug, Deserialize)]
pub struct BinanceTickData {
    pub A: String,
    pub B: String,
    pub E: f64,
    pub T: f64,
    pub a: String,
    pub b: String,
    pub e: String,
    pub s: String,
    pub u: u64,
}

#[derive(Debug, Deserialize)]
pub struct BinanceTick {
    pub data: BinanceTickData,
    pub stream: String
}


pub struct BinanceListenerOptions {
    tickers: Vec<String>,
    // market: FuturesMarket,
}
#[allow(dead_code)]
impl BinanceListenerOptions {
    pub fn new(tickers: Vec<String>) -> BinanceListenerOptions {
        Self { tickers }
    }
}

pub struct BinanceListener {
    // token: Option<String>,
}

impl BinanceListener {
    pub fn new() -> BinanceListener {
        Self {  }
    }

    // pub async fn subscribe(&self, options: BinanceListenerOptions, handler: &Callback<'_>) {
    pub async fn subscribe(&self, options: BinanceListenerOptions) {
        ws_connect(options.tickers).await;
    }
}

// #[allow(dead_code)]
async fn ws_connect(streams: Vec<String>) {
    let (logger_tx, mut logger_rx) =
        tokio::sync::mpsc::unbounded_channel::<WebsocketEvent>();
    let keep_running = AtomicBool::new(true);
    let book_ticker: String = book_ticker_stream("btcusdt");

    let config = Config { ws_endpoint: "wss://fstream.binance.com".into(), ..Config::default() };
    let mut web_socket: WebSockets<'_, CombinedStreamEvent<_>> =
        WebSockets::new_with_options(|event: CombinedStreamEvent<WebsocketEventUntag>| {
            if let WebsocketEventUntag::WebsocketEvent(_we) = &event.data {
                // logger_tx.send(we.clone()).unwrap();
            }
            let data = event.data;
            if let WebsocketEventUntag::BookTicker(orderbook) = data {
                println!("{orderbook:?}");
                // handler(orderbook);
            }
            Ok(())
        }, config);

    let _wait_loop = tokio::spawn(async move {
        loop {
            select! {
                event = logger_rx.recv() => println!("hhhhh {event:?}"),
                // _ = close_rx.recv() => break 'hello
            }
        }
    });

    let endpoints = vec![book_ticker];
    web_socket.connect_multiple(endpoints).await.unwrap(); // check error

    if let Err(e) = web_socket.event_loop(&keep_running).await {
        println!("Error: {e}");
    }
    web_socket.disconnect().await.unwrap();
    println!("disconnected");
}

#[cfg(test)]
mod tests {
    #[test]
    fn some() {
        let list = vec![1, 2, 3];
        println!("Before defining closure: {:?}", list);

        let only_borrows = || println!("From closure: {:?}", list);

        println!("Before calling closure: {:?}", list);
        only_borrows();
        println!("After calling closure: {:?}", list);
    }
}