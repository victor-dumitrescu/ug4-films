module Main

open ParseScript
open Graph
open ToGEXF

open System.IO

let absPath = "C:/Users/Victor/GitHub/base/"
let dirs = absPath
           |> Directory.GetDirectories 
           |> Array.filter (fun x -> match Array.tryFind (fun y -> printfn "%A" y
                                                                   y = x+"/processed\script.xml") (Directory.GetFiles (x+"/processed")) with
                                     | Some _ -> true
                                     | None -> false)

let constructGraph (path: string) = 

    let graph = new CharGraph()

    let scenes = path + "/processed/script.xml" 
                 |> File.ReadAllText
                 |> Script.Parse
                 |> (fun x -> x.Scenes)
                 |> Seq.map processScene
                 |> List.ofSeq

    List.map (addChar graph) scenes |> ignore

    let output = constructXML graph
    let name = sprintf "/../../../output/%s.gexf" (path.[absPath.Length..].Replace(' ', '_'))
    File.WriteAllLines(sprintf "%s%s" (Directory.GetCurrentDirectory()) name, [|output|])


[<EntryPoint>]
let main argv = 
    
    Array.map constructGraph dirs |> ignore
    0
