module File1

open ApiCalls
open Graph
open Microsoft.FSharp.Collections

let queue = ["goodfellas"; "the departed"]
             |> List.map getFilmByTitle 
//             |> List.map (fun x -> (x, List.empty))

[<EntryPoint>]
let main args = 
    
    let seed = Map.empty<Film, Film []>
    let graph = constructGraph seed queue 0
    printfn "%A" graph
    0 // return an integer exit code