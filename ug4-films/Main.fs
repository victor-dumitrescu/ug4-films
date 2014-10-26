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
    let graph = constructGraph seed queue 0
    let output = constructGraph seed queue 0 |> constructXML
    File.WriteAllLines("C:\Users\Victor\GitHub\ug4-films\ug4-films\graph.gefx.xml", [|output|])
    
    //printfn "%A" output
    
    0