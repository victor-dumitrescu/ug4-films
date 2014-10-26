module Main

open ApiCalls
open Graph
open ToGEXF
open Microsoft.FSharp.Collections
open System.IO

let queue = ["goodfellas"; "the departed"]
             |> List.map getFilmByTitle

[<EntryPoint>]
let main args = 
    
    let seed = Map.empty<Film, Film []>
    let output = constructGraph seed queue 0 |> constructXML
    File.WriteAllLines(sprintf "%s%s" (Directory.GetCurrentDirectory()) "/../../../data/rtgraph.gexf", [|output|])

    0