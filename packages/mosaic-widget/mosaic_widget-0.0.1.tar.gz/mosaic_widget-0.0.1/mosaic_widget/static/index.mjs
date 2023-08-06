import * as u from "https://cdn.jsdelivr.net/npm/apache-arrow@11.0.0/+esm";
import { coordinator as d, Coordinator as i, parseJSON as y } from "https://cdn.jsdelivr.net/npm/@uwdata/vgplot@0.0.1/+esm";
let p = 0;
async function m(n) {
  const t = n.model.get("spec");
  console.log("Init client with spec:", t), n.el.classList.add("mosaic-widget");
  const l = {};
  function c(e, r, o) {
    const s = p++;
    l[s] = { query: e, resolve: r, reject: o }, n.model.send({ ...e, queryId: s });
  }
  const a = {
    query(e) {
      return new Promise((r, o) => c(e, r, o));
    }
  };
  n.model.on("msg:custom", (e, r) => {
    console.group(`query ${e.queryId}`), console.log("received message", e, r);
    const o = l[e.queryId];
    switch (delete l[e.queryId], console.log("resolving query", o.query.sql), e.type) {
      case "arrow": {
        const s = u.tableFromIPC(r[0].buffer);
        console.log("table", s), o.resolve(s);
        break;
      }
      case "json": {
        console.log("json", e.result), o.resolve(e.result);
        break;
      }
      default: {
        o.resolve({});
        break;
      }
    }
    console.groupEnd("query");
  }), d(new i(a)), n.el.replaceChildren(await y(t));
}
export {
  m as render
};
