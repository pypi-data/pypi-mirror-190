use std::env;
use std::sync::atomic::{AtomicBool, Ordering};
use std::thread::sleep;
use std::time::{Duration, SystemTime, UNIX_EPOCH};

use binance::futures::websockets::*;
use redis;
use redis::Commands;
use redis::streams::StreamMaxlen;
use serde_json::to_string;

use crate::models::NautilusBookTickerEvent;

pub mod models;

const BINANCE_EVENTS: &str = "quoteticks";

fn main() {
    market_websocket();
}

fn get_current_timestamp_ns() -> u128 {
    let t_now = SystemTime::now();
    let since_the_epoch = t_now
        .duration_since(UNIX_EPOCH).expect("Time went backwards");
    let since_the_epoch_in_nanos = since_the_epoch.as_nanos();
    return since_the_epoch_in_nanos;
}


fn publish_to_redis_stream(
    con: &mut redis::Connection,
    event: NautilusBookTickerEvent,
) -> redis::RedisResult<()> {
    dbg!(&event);
    let maxlen = StreamMaxlen::Approx(10000);
    let event = to_string(&event).unwrap();
    let event_bytes = event.as_bytes();
    let stream_name = "@bookTicker".as_bytes();

    con.xadd_maxlen(
        BINANCE_EVENTS,
        maxlen,
        "*",
        &[
            ("data", event_bytes),
            ("stream", stream_name),
            ("ts_event_ns", get_current_timestamp_ns().to_string().as_bytes())
            // ("ts_event_ns", &get_current_timestamp_ns().to_be_bytes())

        ],
    )?;
    // todo: handle properly
    Ok(())
}


fn market_websocket() {
    let keep_running = AtomicBool::new(true);
    let tickers = vec![
        "1inchusdt", "aaveusdt", "adausdt", "algousdt", "aliceusdt", "ankrusdt", "antusdt", "apeusdt", "atomusdt",
        "avaxusdt", "axsusdt", "balusdt", "bandusdt", "bnbusdt", "bnxusdt", "btcdomusdt", "btcusdt", "compusdt",
        "crvusdt", "darusdt", "dashusdt", "dentusdt", "dogeusdt", "dotusdt", "duskusdt", "dydxusdt", "egldusdt",
        "eosusdt", "etcusdt", "ethusdt", "filusdt", "flmusdt", "flowusdt", "ftmusdt", "galausdt", "galusdt", "gmtusdt",
        "grtusdt", "hntusdt", "hotusdt", "imxusdt", "iostusdt", "iotausdt", "iotxusdt", "kavausdt", "klayusdt",
        "kncusdt", "ksmusdt", "linausdt", "linkusdt", "litusdt", "lrcusdt", "ltcusdt", "manausdt", "maskusdt",
        "maticusdt", "nearusdt", "oceanusdt", "ognusdt", "omgusdt", "oneusdt", "ontusdt", "peopleusdt", "reefusdt",
        "renusdt", "rlcusdt", "roseusdt", "runeusdt", "sandusdt", "sklusdt", "snxusdt", "solusdt", "stmxusdt",
        "storjusdt", "sushiusdt", "uniusdt", "vetusdt", "wavesusdt", "woousdt", "xlmusdt", "xmrusdt", "xrpusdt",
        "yfiusdt"];

    let stream_tickers: Vec<String> = tickers.iter().map(|t| format!("{}@bookTicker", t)).collect();
    dbg!(&stream_tickers);

    let redis_url = env::var("REDIS_URL").unwrap_or("redis://127.0.0.1/".to_string());

    loop {
        let client = redis::Client::open(redis_url.clone()).unwrap();
        let con_result = client.get_connection();
        match con_result {
            Ok(mut con) => {
                let mut callback_fn = |event: FuturesWebsocketEvent| {
                    dbg!(&event);

                    if let FuturesWebsocketEvent::BookTicker(e) = event {
                        let nautilus_event: NautilusBookTickerEvent = e.into();
                        publish_to_redis_stream(&mut con, nautilus_event).unwrap_or_else(|e| { dbg!(&e); });
                    }

                    Ok(())
                };

                // println!("Starting with USD_M {:?}", stream_example);
                keep_running.swap(true, Ordering::Relaxed);

                let mut web_socket: FuturesWebSockets<'_> = FuturesWebSockets::new(&mut callback_fn);
                web_socket
                    .connect_multiple_streams(&FuturesMarket::USDM, &stream_tickers[..])
                    .unwrap();

                if let Err(e) = web_socket.event_loop(&keep_running) {
                    match e {
                        err => {
                            println!("Error: {:?}", err);
                        }
                    }
                }
                web_socket.disconnect().unwrap();
            }
            Err(err) => {
                dbg!("Error happen with rediska. Reconnecting...");
                dbg!(err);
                sleep(Duration::new(10, 0));
            }
        }
    }
}
