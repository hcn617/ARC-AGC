use proconio::input;
use std::cmp::min;

fn main() {
    input! {
        n:usize, a:usize, b:usize,
    }
    // n < a のとき、Aliceは一度も操作できずに全ゲームで負け。
    if n < a {
        println!("0");
        return;
    }

    // a <= b のとき、ゲームa ～ ゲームn でAliceの勝ち。
    if a <= b {
        println!("{}", n - a + 1);
        return;
    }

    // a > b のとき、loop * b + min(zan, b)
    let loop_cnt = n / a - 1;
    let zan = 1 + n % a;
    let ans = loop_cnt * b + min(zan, b);
    println!("{}", ans);
    // println!("{}, {}", loop_cnt, zan);
}
