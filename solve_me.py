from http.server import BaseHTTPRequestHandler, HTTPServer


class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items = {}
    completed_items = []

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            self.completed_items = file.readlines()
            file.close()
        except Exception:
            pass

    def write_current(self):
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def runserver(self):
        address = "127.0.0.1"
        port = 8000
        server_address = (address, port)
        httpd = HTTPServer(server_address, TasksServer)
        print(f"Started HTTP Server on http://{address}:{port}")
        httpd.serve_forever()

    def run(self, command, args):
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "runserver":
            self.runserver()
        elif command == "help":
            self.help()

    def help(self):
        print(
            """Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics
$ python tasks.py runserver # Starts the tasks management server"""
        )

    def add(self, args):
        priority = int(args[0])
        task = args[1]

        def modifyPriority(priority):
            if priority+1 in self.current_items.keys():
                priority = priority+1
                modifyPriority(priority)
            else:
                self.current_items[priority+1] = self.current_items[priority]
                del self.current_items[priority]

        def addTaskWithPriority(priority, task):
            self.current_items[priority] = task
            self.write_current()
            print('Added task: "{}" with priority {}'.format(task, priority))

        def PriorityCheck(priority, task):
            while priority in self.current_items.keys():
                modifyPriority(priority)
            addTaskWithPriority(priority, task)

        PriorityCheck(priority, task)

    def done(self, args):
        priority = int(args[0])

        def addCompletedTask(task):
            self.completed_items.append(task)
            self.write_completed()

        if priority in self.current_items.keys():
            task = self.current_items[priority]
            addCompletedTask(task)
            del self.current_items[priority]
            self.write_current()
            print("Marked item as done.")
        else:
            print(
                f"Error: no incomplete item with priority {priority} exists.")

    def delete(self, args):
        priority = int(args[0])
        if priority in self.current_items.keys():
            del self.current_items[priority]
            self.write_current()
            print(f"Deleted item with priority {priority}")
        else:
            print(
                f"Error: item with priority {priority} does not exist. Nothing deleted.")

    def ls(self):
        self.read_current()
        listString = []
        for index, priority in enumerate(sorted(self.current_items.keys())):
            listString.append(
                f"{index+1}. {self.current_items[priority]} {[priority]}\n")
        listString[len(listString) -
                   1] = listString[len(listString)-1].rstrip("\n")
        for listTask in listString:
            print(listTask, end="")

    def report(self):
        self.read_current()
        self.read_completed()
        pendingTaskCount = len(self.current_items)
        completedTaskCount = len(self.completed_items)
        pendingString = f"Pending : {pendingTaskCount}\n"
        completedString = f"Completed : {completedTaskCount}\n"
        for index, priority in enumerate(sorted(self.current_items)):
            pendingString = pendingString + \
                f"{index+1}. {self.current_items[priority]} {[priority]}\n"
        for index, task in enumerate(sorted(self.completed_items)):
            completedString = completedString + \
                f"{index+1}. {self.completed_items[index]}\n"
        finalString = pendingString+"\n"+completedString.rstrip("\n")
        print(finalString, end="")

    def render_pending_tasks(self):
        # Complete this method to return all incomplete tasks as HTML
        self.read_current()
        self.read_completed()
        pendingString = ""
        for priority in sorted(self.current_items):

            # Pending task page HTML implementation

            pendingString = pendingString + \
                f"""
<li class="flex py-4 first:pt-0 last:pb-0 ">
   <img class="h-30 w-20 rounded-full" src="https://icon-library.com/images/task-icon-png/task-icon-png-24.jpg" alt="" />
   <div class="ml-3 overflow-hidden">
      <p class="text-xl font-medium text-slate-900">Name: {self.current_items[priority]}</p>
      <p class="text-sm text-slate-500 truncate">Priority: #{priority}</p>
   </div>
</li>       
                """
        pendingHtml = f"""
<!doctype html>
<html>
   <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <script src="https://cdn.tailwindcss.com"></script>
   </head>
   <body>
      <div class="grid grid-cols-1 divide-y">
         <div class="bg-slate-900 flex justify-start" >
            <div class="mb-2 mt-2 ml-3">
               <h1 class="mt-3 text-2xl font-bold text-slate-50"><a href="#">Task
                  <span class="before:block before:absolute before:-inset-1 before:-skew-y-3 before:bg-green-500 relative inline-block">
                  <span class="relative text-white">Manager</span>
                  </span>
                  </a>
               </h1>
            </div>
            <div class="ml-6 sm:visible md:visible lg:visible"><button class="border-2 rounded-full border-rose-500 bg-rose-500 text-slate-50 text-1xl mt-5 px-3">
               <a href="http://localhost:8000/tasks">Pending <span class="font-bold">{len(self.current_items)}</span></a></button>
            </div>
            <div class="ml-6"><button class="border-2 rounded-full border-green-500 bg-green-500 text-slate-50 text-1xl mt-5 px-3">
               <a href="http://localhost:8000/completed">Completed <span class="font-bold">{len(self.completed_items)}</span></a></button>
            </div>
            <br><br><br>
         </div>
         <div class="grid lg:grid-cols-2 sm:grid-cols-1 gap-4">
            <div>
               <br><br>
               <blockquote class="text-2xl font-semibold italic text-center text-slate-900">
                  Manage your Tasks
                  <span class="before:block before:absolute before:-inset-1 before:-skew-y-3 before:bg-pink-500 relative inline-block">
                  <span class="relative text-white">like a pro</span>
                  </span>
                  with us, don't worry we got your back.
               </blockquote>
               <img src="https://vectorforfree.com/wp-content/uploads/2020/03/Working_Men_VectorForFree.png" />
            </div>
            <div>
               <div class="text-center">
                  <div class="border-2 border-orange-500 px-2 py-2  mt-4 mx-2" style="height="auto">
                     <h1 class="text-orange-500 text-2xl font-bold">
                        Incomplete Tasks
                     </h1>
                     <ul role="list" class="p-6 divide-y divide-orange-500">
                        {pendingString}
                     </ul>
                  </div>
               </div>
            </div>
         </div>
      </div>
   </body>
</html>
        """
        return f"{pendingHtml}"

    def render_completed_tasks(self):
        # Complete this method to return all completed tasks as HTML
        self.read_completed()
        self.read_current()
        completedString = ""
        for index, completed_task in enumerate(sorted(self.completed_items)):

            # Completed task page HTML implementation

            completedString = completedString + \
                f"""
                <li class="flex py-4 first:pt-0 last:pb-0 ">
   <img class="h-30 w-20 rounded-full" src="https://icon-library.com/images/task-icon-png/task-icon-png-24.jpg" alt="" />
   <div class="ml-3 overflow-hidden">
      <p class="text-xl font-medium text-slate-900">Name: {completed_task}</p>
      <p class="text-sm text-slate-500 truncate">Number: #{index+1}</p>
   </div>
</li>
                """
        completedHtml = f"""
<!doctype html>
<html>
   <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <script src="https://cdn.tailwindcss.com"></script>
   </head>
   <body>
      <div class="grid grid-cols-1 divide-y">
         <div class="bg-slate-900 flex justify-start" >
            <div class="mb-2 mt-2 ml-3">
               <h1 class="mt-3 text-2xl font-bold text-slate-50"><a href="#">Task
                  <span class="before:block before:absolute before:-inset-1 before:-skew-y-3 before:bg-green-500 relative inline-block">
                  <span class="relative text-white">Manager</span>
                  </span>
                  </a>
               </h1>
            </div>
            <div class="ml-6 sm:visible md:visible lg:visible"><button class="border-2 rounded-full border-rose-500 bg-rose-500 text-slate-50 text-1xl mt-5 px-3">
               <a href="http://localhost:8000/tasks">Pending <span class="font-bold">{len(self.current_items)}</span></a></button>
            </div>
            <div class="ml-6"><button class="border-2 rounded-full border-green-500 bg-green-500 text-slate-50 text-1xl mt-5 px-3">
               <a href="http://localhost:8000/completed">Completed <span class="font-bold">{len(self.completed_items)}</span></a></button>
            </div>
            <br><br><br>
         </div>
         <div class="grid lg:grid-cols-2 sm:grid-cols-1 gap-4">
            <div>
               <br><br>
               <blockquote class="text-2xl font-semibold italic text-center text-slate-900">
                  Manage your Tasks
                  <span class="before:block before:absolute before:-inset-1 before:-skew-y-3 before:bg-pink-500 relative inline-block">
                  <span class="relative text-white">like a pro</span>
                  </span>
                  with us, don't worry we got your back.
               </blockquote>
               <img src="https://vectorforfree.com/wp-content/uploads/2020/03/Working_Men_VectorForFree.png" />
            </div>
            <div>
               <div class="text-center">
                  <div class="border-2 border-orange-500 px-2 py-2  mt-4 mx-2" style="height="auto">
                     <h1 class="text-orange-500 text-2xl font-bold">
                        Completed Tasks
                     </h1>
                     <ul role="list" class="p-6 divide-y divide-orange-500">
                        {completedString}
                     </ul>
                  </div>
               </div>
            </div>
         </div>
      </div>
   </body>
</html>
        """
        return f"{completedHtml}"


class TasksServer(TasksCommand, BaseHTTPRequestHandler):
    def do_GET(self):
        task_command_object = TasksCommand()
        if self.path == "/tasks":
            content = task_command_object.render_pending_tasks()
        elif self.path == "/completed":
            content = task_command_object.render_completed_tasks()
        else:
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())
