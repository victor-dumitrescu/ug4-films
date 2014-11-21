module Main

open ParseScript
open Graph
open ToGEXF

open System.IO

[<EntryPoint>]
let main argv = 
    
    let graph = new CharGraph()

    let scenes = "C:/Users/Victor/GitHub/base/The Silence of the Lambs (film)/processed/script.xml" 
                 |> File.ReadAllText
                 |> Script.Parse
                 |> (fun x -> x.Scenes)
                 |> Seq.map processScene
                 |> List.ofSeq

    List.map (addChar graph) scenes |> ignore

    let output = constructXML graph
    File.WriteAllLines(sprintf "%s%s" (Directory.GetCurrentDirectory()) "/../../../data/naivegraph.gexf", [|output|])

    0
