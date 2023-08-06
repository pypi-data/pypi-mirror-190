use serde::{Deserialize, Serialize};
use std::convert::From;
use binance::model::BookTickerEvent;


#[allow(non_snake_case)]
#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct NautilusBookTickerEvent {
    pub u: u64,     // update_id
    pub s: String,  // symbol
    pub b: String,  // bid
    pub B: String,  // bid_size
    pub a: String,  // ask
    pub A: String,  // ask_size
}

impl From<BookTickerEvent> for NautilusBookTickerEvent {
    // todo: convert to nautilus format: 'from nautilus_trader.adapters.binance.futures.data.BinanceFuturesDataClient import _handle_book_ticker'
    fn from(event: BookTickerEvent) -> NautilusBookTickerEvent {
        NautilusBookTickerEvent {
            u: event.update_id,
            s: event.symbol,
            b: event.best_bid,
            B: event.best_bid_qty,
            a: event.best_ask,
            A: event.best_ask_qty,
        }
    }
}

#[allow(non_snake_case)]
#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct TickData {
    // update_id
    pub u: u64,
    // symbol
    pub s: String,
    // bid
    pub b: String,
    // bid_size
    pub B: String,
    // ask
    pub a: String,
    // ask_size
    pub A: String,
}

// impl From<BookTickerEvent> for TickData {
//     // todo: convert to nautilus format: 'from nautilus_trader.adapters.binance.futures.data.BinanceFuturesDataClient import _handle_book_ticker'
//     fn from(event: BookTickerEvent) -> TickData {
//         TickData {
//             u: event.update_id,
//             s: event.symbol,
//             b: event.best_bid,
//             B: event.best_bid_qty,
//             a: event.best_ask,
//             A: event.best_ask_qty,
//         }
//     }
// }