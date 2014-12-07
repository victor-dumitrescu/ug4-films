module Graph

open ApiCalls


type FilmGraph = Map<Film, Film []>
let maxLevel = 95

let unwrapOption (x: Film [] option) =
    match x with
        | Some fl -> List.ofArray fl
        | None    -> []

let addToExisting (film: Film) (graph: FilmGraph) (elem: Film) =
    //if elem is a member of the graph, add the new edge from elem to film
    if graph.ContainsKey elem then
        let sim = graph.Item elem
        let sim' =
            if Array.exists (fun x -> x = film) sim then
                sim
            else
                Array.append sim [|film|]
        (graph.Remove elem).Add (elem, sim')
    else
        graph

//new films can be added to the graph, but only up to a certain level
let rec constructGraph (graph: FilmGraph) (queue: Film list) (level: int)=
    if not queue.IsEmpty then
        printfn "%A %A" queue.Head level
    match queue with
    | [] -> graph
    | q ->  match (graph.ContainsKey q.Head) with
            | true -> constructGraph graph q.Tail level
            | false ->  let similar = q.Head.id |> getSimilarFilms
                        match similar with
                        | Some sim -> if (level = maxLevel) then
                                          // Max level reached, do not introduce any new films (not already in the graph)
                                          let sim' = Array.filter (fun x -> graph.ContainsKey x) sim
                                          let (graph': FilmGraph) = Array.fold (addToExisting q.Head) (graph.Add (q.Head, sim')) sim'
                                          constructGraph graph' q.Tail level
                                      else
                                          let (graph': FilmGraph) = Array.fold (addToExisting q.Head) (graph.Add (q.Head, sim)) sim
                                          constructGraph graph' (List.append q.Tail (List.ofArray sim)) (level+1)
                        | None -> constructGraph graph q.Tail level

// a version of constructGraph where no new films can be introduced in the graph
let rec constructGraph2 (graph: FilmGraph) (queue: Film list)=
    match queue with
    | [] -> graph
    | q ->  match (graph.ContainsKey q.Head) with
            | true -> constructGraph2 graph q.Tail
            | false ->  let similar = q.Head.id |> getSimilarFilms
                        match similar with
                        | Some sim -> let sim' = Array.filter (fun x -> List.exists (fun y -> y=x) queue) sim
                                      let (graph': FilmGraph) = Array.fold (addToExisting q.Head) (graph.Add (q.Head, sim')) sim'
                                      constructGraph2 graph' q.Tail
                        | None -> constructGraph2 graph q.Tail

let rec constructGraph3 (graph: FilmGraph) (queue: Film list)=
    constructGraph graph queue 0