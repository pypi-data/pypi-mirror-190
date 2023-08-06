#FROM rust-lang/rust:nightly-buster as build
FROM rustlang/rust:nightly as build

# create a new empty shell project
RUN USER=root cargo new --bin exchange_worker
WORKDIR /exchange_worker

RUN echo $(cargo -V)
RUN file="$(cargo -V)" && echo $file

# to cache deps
COPY ./Cargo.lock ./Cargo.lock
COPY ./Cargo.toml ./Cargo.toml
#RUN cargo build --release
RUN cargo build -r --bin exchange_worker_cli
RUN rm src/*.rs

# current sorce files
COPY ./src ./src

# build for release
RUN rm ./target/release/deps/exchange_worker*
RUN cargo build --release

# our final base
FROM gcr.io/distroless/cc

# Get Build Hash From CI
ARG BUILD_HASH
ENV REVISION=$BUILD_HASH

# copy the build artifact from the build stage
COPY --from=build /exchange_worker/target/release/exchange_worker_cli .

# set the startup command to run your binary
CMD ["./exchange_worker_cli"]
