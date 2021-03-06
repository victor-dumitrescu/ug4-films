﻿module Main

open ApiCalls
open Graph
open ToGEXF
open Microsoft.FSharp.Collections
open System.IO

let absPath = "C:/Users/Victor/GitHub/base/"
let dirs = absPath
           |> Directory.GetDirectories 
           |> Array.filter (fun x -> match Array.tryFind (fun y -> y = x+"/processed\script.xml") (Directory.GetFiles (x+"/processed")) with
                                     | Some _ -> true
                                     | None -> false)
           |> Array.map (fun x -> x.[absPath.Length..])
           |> Array.map (fun x -> if x.Length >= 5 && x.[x.Length-5..] = "film)" then x.[..x.Length-7] else x)

let dirs2 = [|"goodfellas"; "analyze that"; "trainspotting"; "gone with the wind"; "a beautiful mind"|]

let queue = dirs
             |> Array.map getFilmByTitle
             |> Array.filter (fun x -> x.IsSome)
             |> Array.map (fun x -> x.Value)
             |> List.ofArray

[<EntryPoint>]
let main args = 
    
    let seed = Map.empty<Film, Film []>
    let output = constructGraph3 seed queue |> constructXML
    File.WriteAllLines(sprintf "%s%s" (Directory.GetCurrentDirectory()) "/../../../data/rtgraph3.gexf", [|output|])

    0